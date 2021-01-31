import datetime as dt
from os import getenv
from random import randint, shuffle

from flask import Flask, g, jsonify, redirect, request, send_from_directory

from gibble.helpers import (
    game_duration,
    make_grid_array,
    score_game,
    score_word,
)

def create_app():
    app = Flask(__name__, static_url_path='')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv(
        'DATABASE_URL',
        'sqlite:///gibble.db',
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from gibble.models import Game, GamePlayer, User, Word, WordRejection, db
    db.init_app(app)

    @app.before_request
    def authenticate():
        user_id = request.cookies.get('user_id')
        if user_id is not None:
            user = db.session.query(User).filter_by(id=user_id).first()
            if user is None:
                return {'error': 'Unknown user_id'}, 401
        else:
            user = None
        g.user = user

    @app.route('/', methods=['GET'])
    def reroute():
        return redirect('/menu.html', code=302)

    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        user = db.session.query(User).filter_by(username=username).first()
        if user is None:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        user_id = str(user.id)
        response = jsonify({'user_id': user_id, 'username': username})
        response.set_cookie('user_id', user_id)
        response.set_cookie('username', username)
        return response

    @app.route('/games', methods=['POST'])
    def create_game():
        dice_slots = list(range(16))
        shuffle(dice_slots)
        faces = [randint(0, 5) for _ in range(16)]
        dice = [
            'AACIOT',
            'ABILTY',
            'ABJMOQ',
            'ACDEMP',
            'ACELRS',
            'ADENVZ',
            'AHMORS',
            'BIFORX',
            'DENOSW',
            'DKNOTU',
            'EEFHIY',
            'EGKLUY',
            'EGINTV',
            'EHINPS',
            'ELPSTU',
            'GILRUW',
        ]
        grid = ''.join(dice[d][f] for d, f in zip(dice_slots, faces))
        game = Game(grid=grid)
        game_player = GamePlayer(user_id=g.user.id)
        game.game_players.append(game_player)
        db.session.add(game)
        db.session.commit()
        return {'id': game.id}

    @app.route('/games', methods=['GET'])
    def get_games():
        if g.user is None:
            return {'error': 'Missing user_id'}, 401
        game_ids = [gp.game_id for gp in g.user.game_players]
        games = (
            db.session.query(GamePlayer)
            .options(
                db.joinedload(GamePlayer.game)
                .subqueryload(Game.game_players)
                .joinedload(GamePlayer.user)
            )
            .filter(GamePlayer.user_id == g.user.id)
            .all()
        )
        timelimit = dt.datetime.now() - game_duration()
        return {
            'games': [
                {
                    'id': gp.game.id,
                    'created_at': gp.game.created_at,
                    'played': gp.has_played,
                    'players': [
                        {
                            'id': gp_.user.id,
                            'username': gp_.user.username,
                            'played': gp_.has_played,
                        }
                        for gp_ in gp.game.game_players
                    ],
                }
                for gp in games
            ],
        }

    @app.route('/games/<int:game_id>', methods=['POST'])
    def join_game(game_id):
        if g.user is None:
            return {'error': 'Missing user_id'}, 401
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(user_id=g.user.id, game_id=game_id)
            .first_or_404()
        )
        flat_grid = game_player.game.grid
        grid = make_grid_array(flat_grid)
        now = dt.datetime.now()
        if game_player.started_at is None:
            game_player.started_at = now
            db.session.commit()
        time_elapsed = now - game_player.started_at
        seconds_remaining = int(
            (game_duration() - time_elapsed).total_seconds()
        )
        words = [word.word for word in game_player.words]
        return {
            'grid': grid,
            'seconds_remaining': max(seconds_remaining, 0),
            'words_played': words,
        }

    @app.route('/games/<int:game_id>', methods=['GET'])
    def get_single_game(game_id):
        if g.user is None:
            return {'error': 'Missing user_id'}, 401
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(user_id=g.user.id, game_id=game_id)
            .first_or_404()
        )
        has_played = game_player.has_played
        base_join = db.joinedload(Game.game_players)
        joins = (
            (base_join.joinedload(GamePlayer.user),)
            + (base_join.joinedload(GamePlayer.words),)
            + (base_join.joinedload(GamePlayer.word_rejections),)
        )
        game = (
            db.session.query(Game).options(*joins)
            .filter(Game.id == game_id)
            .first()
        )
        users = [
            {'id': gp.user.id, 'username': gp.user.username}
            for gp in game.game_players
        ]
        words = has_played and [
            {
                'word': word.word,
                'user_id': gp.user.id,
                'score': score_word(word.word),
            }
            for gp in game.game_players
            for word in gp.words
        ] or []
        vetoes = has_played and [
            {'word': rejection.word, 'user_id': gp.user.id}
            for gp in game.game_players
            for rejection in gp.word_rejections
        ] or []
        player_scores = score_game(words, vetoes)
        grid = (
            has_played
            and make_grid_array(game.grid)
            or make_grid_array('?' * 16)
        )
        return {
            'id': game.id,
            'grid': grid,
            'played': has_played,
            'created_at': game.created_at,
            'users': users,
            'words': words,
            'scores': player_scores,
            'vetoes': vetoes,
        }

    @app.route('/games/<int:game_id>/players', methods=['POST'])
    def challenge(game_id):
        if g.user is None:
            return {'error': 'Missing user_id'}, 401
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(user_id=g.user.id, game_id=game_id)
            .first_or_404()
        )
        opponent_username = request.json.get('username')
        if opponent_username is None:
            return {'error': 'Missing username for opponent'}, 400
        opponent = (
            db.session.query(User)
            .filter_by(username=opponent_username)
            .first_or_404()
        )
        challenge_exists = (
            db.session.query(GamePlayer)
            .filter_by(user_id=opponent.id, game_id=game_id)
            .first()
        ) is not None
        if not challenge_exists:
            opponent_game_player = GamePlayer(
                user_id=opponent.id,
                game_id=game_id,
            )
            db.session.add(opponent_game_player)
            db.session.commit()
        return {'id': opponent.id, 'username': opponent.username}

    @app.route('/games/<int:game_id>/players', methods=['GET'])
    def get_game_players(game_id):
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(game_id=game_id, user_id=g.user.id)
            .filter(GamePlayer.started_at.isnot(None))
            .first_or_404()
        )
        game_players = (
            db.session.query(User)
            .join(GamePlayer, GamePlayer.user_id == User.id)
            .filter(GamePlayer.game_id == game_id)
            .all()
        )
        return {'players': [
            {'id': player.id, 'username': player.username}
            for player in game_players
        ]}

    @app.route('/games/<int:game_id>/words', methods=['POST'])
    def submit_words(game_id):
        TIMELIMIT = game_duration(buffer_=True)
        words = request.json.get('words')
        game_player = (
            db.session.query(GamePlayer)
            .filter(
                GamePlayer.game_id==game_id,
                GamePlayer.user_id==g.user.id,
                GamePlayer.started_at.isnot(None),
            )
            .first_or_404()
        )
        if dt.datetime.now() - game_player.started_at > TIMELIMIT:
            return {'error': 'Timer expired'}, 400
        existing_words = {word.word for word in (
            db.session.query(Word)
            .filter_by(game_player_id=game_player.id)
            .all()
        )}
        db_words = [
            Word(word=word.upper(), game_player_id=game_player.id)
            for word in words
            if word.upper() not in existing_words
        ]
        db.session.add_all(db_words)
        db.session.commit()
        return {}, 201

    @app.route('/games/<int:game_id>/words', methods=['GET'])
    def get_words(game_id):
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(game_id=game_id, user_id=g.user.id)
            .first_or_404()
        )
        TIMELIMIT = game_duration(buffer_=True)
        complete = (
            game_player.started_at is not None
            and dt.datetime.now() - game_player.started_at > TIMELIMIT
        )
        words = (
            db.session.query(
                Word.word,
                GamePlayer.user_id,
            )
            .join(GamePlayer, GamePlayer.id == Word.game_player_id)
            .filter(GamePlayer.game_id == game_id)
            .all()
        )
        users = (
            db.session.query(User.id, User.username)
            .filter(User.id.in_(word.user_id for word in words))
            .all()
        )
        return {
            'words': complete and [
                {'word': word.word, 'user_id': word.user_id}
                for word in words
            ] or [],
            'users': [
                {'id': user.id, 'username': user.username}
                for user in users
            ],
        }

    @app.route('/games/<int:game_id>/vetoes', methods=['POST'])
    def veto_word(game_id):
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(game_id=game_id, user_id=g.user.id)
            .filter(GamePlayer.started_at.isnot(None))
            .first_or_404()
        )
        word = request.json.get('word')
        existing_veto = db.session.query(WordRejection).get(
            {'word': word, 'game_player_id': game_player.id},
        )
        if existing_veto is None:
            veto = WordRejection(word=word, game_player_id=game_player.id)
            db.session.add(veto)
            db.session.commit()
        else:
            db.session.delete(existing_veto)
            db.session.commit()
        vetoes = (
            db.session.query(WordRejection.word, GamePlayer.user_id)
            .join(GamePlayer, GamePlayer.id == WordRejection.game_player_id)
            .filter(GamePlayer.game_id == game_id)
            .all()
        )
        return {'vetoes': [
            {'word': veto.word, 'user_id': veto.user_id}
            for veto in vetoes
        ]}

    @app.route('/games/<int:game_id>/vetoes', methods=['GET'])
    def get_vetoes(game_id):
        game_player = (
            db.session.query(GamePlayer)
            .filter_by(game_id=game_id, user_id=g.user.id)
            .filter(GamePlayer.started_at.isnot(None))
            .first_or_404()
        )
        vetoes = (
            db.session.query(WordRejection.word, GamePlayer.user_id)
            .join(GamePlayer, GamePlayer.id == WordRejection.game_player_id)
            .filter(GamePlayer.game_id == game_id)
            .all()
        )
        return {'vetoes': [
            {'word': veto.word, 'user_id': veto.user_id}
            for veto in vetoes
        ]}

    @app.cli.command('init-db')
    def init_db():
        """Create the database tables."""
        with app.app_context():
            db.create_all()

    @app.cli.command('reset-db')
    def reset_db():
        """Drop and recreate the database tables."""
        with app.app_context():
            db.drop_all()
            db.create_all()

    return app
