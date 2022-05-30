import datetime as dt

from flask_sqlalchemy import SQLAlchemy

from gibble.helpers import game_duration

db = SQLAlchemy()


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, default=dt.datetime.now)
    game_players = db.relationship("GamePlayer", lazy=True, backref="game")
    puzzle_word = db.Column(db.String(16))
    puzzle_hint = db.Column(db.String(256))

    def __repr__(self):
        return f"<Game {self.id}: {self.grid[:8]}...>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    game_players = db.relationship("GamePlayer", lazy=True, backref="user")

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class GamePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), index=True)
    started_at = db.Column(db.DateTime)

    unique_game_player = db.UniqueConstraint("user_id", "game_id")

    @property
    def has_played(self):
        timelimit = dt.datetime.now() - game_duration()
        return self.started_at is not None and self.started_at < timelimit


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_player_id = db.Column(
        db.Integer,
        db.ForeignKey("game_player.id"),
        index=True,
        nullable=False,
    )
    word = db.Column(db.String(17), nullable=False)
    submitted_at = db.Column(db.DateTime, default=dt.datetime.now)
    game_player = db.relationship("GamePlayer", lazy=False, backref="words")

    unique_game_player_word = db.UniqueConstraint("game_player_id", "word")

    def __repr__(self):
        if self.game_player is not None:
            username = self.game_player.user.username
        else:
            username = None
        return f"<Word {self.id}: {self.word}, {username}>"


class WordRejection(db.Model):
    word = db.Column(db.String(17), primary_key=True)
    game_player_id = db.Column(
        db.Integer,
        db.ForeignKey("game_player.id"),
        primary_key=True,
    )
    game_player = db.relationship("GamePlayer", lazy=True, backref="word_rejections")
