from collections import Counter
import datetime as dt
from random import randint, shuffle
from typing import List, Optional


SIZE = 4

DICE = [
    "AACIOT",
    "ABILTY",
    "ABJMOQ",
    "ACDEMP",
    "ACELRS",
    "ADENVZ",
    "AHMORS",
    "BIFORX",
    "DENOSW",
    "DKNOTU",
    "EEFHIY",
    "EGKLUY",
    "EGINTV",
    "EHINPS",
    "ELPSTU",
    "GILRUW",
]


def game_duration(buffer_=False):
    return dt.timedelta(minutes=3, seconds=10 * buffer_)


def make_grid_array(flat_grid):
    grid = [[None] * SIZE for _ in range(SIZE)]
    for i, letter in enumerate(flat_grid):
        grid[i // SIZE][i % SIZE] = letter
    return grid


def score_word(word):
    score_map = {
        3: 1,
        4: 1,
        5: 2,
        6: 3,
        7: 5,
        8: 11,
    }
    length = len(word)
    score = score_map.get(length, 0 if length < 3 else 11)
    return score


def score_game(words, vetoes):
    """words: {word, user_id, score}"""
    veto_counts = Counter(veto["word"] for veto in vetoes)
    player_scores = {word["user_id"]: 0 for word in words}
    word_counts = Counter(word["word"] for word in words)
    unique_words = set(word for word, count in word_counts.items() if count == 1)
    veto_threshold = int(len(player_scores.keys()) / 2 + 0.5)
    for word in words:
        veto_count = veto_counts.get(word["word"], 0)
        vetoed = veto_count >= veto_threshold or any(
            v["user_id"] == word["user_id"] and v["word"] == word["word"]
            for v in vetoes
        )
        if word["word"] in unique_words and not vetoed:
            player_scores[word["user_id"]] += word["score"]
    player_scores_list = [
        {"user_id": user_id, "score": score} for user_id, score in player_scores.items()
    ]
    return player_scores_list


def get_neighbor_indices(index: int) -> List[int]:
    candidates = (
        index + SIZE * j + i for j in (-1, 0, 1) for i in (-1, 0, 1) if (i, j) != (0, 0)
    )
    x = index % SIZE
    return [c for c in candidates if 0 <= c < SIZE**2 and abs((c % SIZE) - x) <= 1]


def extend_path(path: List[int]) -> List[List[int]]:
    tail = path[-1]
    return [
        path + [candidate]
        for candidate in get_neighbor_indices(tail)
        if candidate not in path
    ]


def get_one_path(word_length: int) -> list[int]:
    path = []
    frontiers: list[list[int]] = []
    frontiers.append([y * SIZE + x for y in range(int(SIZE)) for x in range(int(SIZE))])
    while len(path) < word_length:
        while not frontiers[-1]:
            frontiers.pop()
            if not frontiers:
                raise ValueError(f"Cannot create path of length {word_length}")
            path.pop()
        new_tile_index = randint(0, len(frontiers[-1]) - 1)
        path.append(frontiers[-1].pop(new_tile_index))
        frontiers.append(
            [
                candidate
                for candidate in get_neighbor_indices(path[-1])
                if candidate not in path
            ]
        )
    return path


def generate_grid(puzzle_word: Optional[str]) -> str:
    dice_slots = list(range(SIZE**2))
    shuffle(dice_slots)
    faces = [die[randint(0, 5)] for die in DICE]
    slots = [faces[slot] for slot in dice_slots]
    if puzzle_word:
        puzzle_path = get_one_path(len(puzzle_word))
        for index, character in zip(puzzle_path, puzzle_word.upper()):
            slots[index] = character
    grid = "".join(slots)
    return grid
