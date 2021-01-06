from collections import Counter
import datetime as dt


def game_duration(buffer_=False):
    return dt.timedelta(minutes=3, seconds=10 * buffer_)


def make_grid_array(flat_grid):
    grid = [[None] * 4 for _ in range(4)]
    for i, letter in enumerate(flat_grid):
        grid[i // 4][i % 4] = letter
    return grid


def score_word(word):
    score_map = {
        3: 1,
        4: 1,
        5: 2,
        6: 3,
        7: 4,
        8: 11,
    }
    length = len(word)
    score = score_map.get(length, 0 if length < 3 else 11)
    return score


def score_game(words, vetoes):
    '''words: {word, user_id, score}'''
    veto_counts = Counter(veto['word'] for veto in vetoes)
    player_scores = {word['user_id']: 0 for word in words}
    word_counts = Counter(word['word'] for word in words)
    unique_words = set(
        word
        for word, count in word_counts.items()
        if count == 1
    )
    veto_threshold = int(len(player_scores.keys()) / 2 + 0.5)
    for word in words:
        veto_count = veto_counts.get(word['word'], 0)
        vetoed = (
            veto_count >= veto_threshold
            or any(
                v['user_id'] == word['user_id']
                and v['word'] == word['word']
                for v in vetoes
            )
        )
        if word['word'] in unique_words and not vetoed:
            player_scores[word['user_id']] += word['score']
    player_scores_list = [
        {'user_id': user_id, 'score': score}
        for user_id, score in player_scores.items()
    ]
    return player_scores_list
