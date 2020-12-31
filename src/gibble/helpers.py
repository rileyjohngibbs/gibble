from collections import Counter


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


def score_game(words):
    '''words: {word, user_id, score}'''
    player_scores = {word['user_id']: 0 for word in words}
    word_counts = Counter(word['word'] for word in words)
    unique_words = set(
        word
        for word, count in word_counts.items()
        if count == 1
    )
    for word in words:
        if word['word'] in unique_words:
            player_scores[word['user_id']] += word['score']
    player_scores_list = [
        {'user_id': user_id, 'score': score}
        for user_id, score in player_scores.items()
    ]
    return player_scores_list
