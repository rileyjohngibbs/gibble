import pytest

from gibble.helpers import get_neighbor_indices, extend_path

index_neighbors = [
    (0, {1, 4, 5}),
    (3, {2, 6, 7}),
    (12, {8, 9, 13}),
    (15, {10, 11, 14}),
]


@pytest.mark.parametrize('index,expected_neighbors', index_neighbors)
def test_corner_neighbors(index, expected_neighbors):
    neighbors = get_neighbor_indices(index)
    assert set(neighbors) == expected_neighbors


edge_index_neighbors = [
    (1, {0, 2, 4, 5, 6}),
    (11, {6, 7, 10, 14, 15}),
]


@pytest.mark.parametrize('index,expected_neighbors', edge_index_neighbors)
def test_edge_neighbors(index, expected_neighbors):
    neighbors = get_neighbor_indices(index)
    assert set(neighbors) == expected_neighbors


def test_middle_neighbors():
    neighbors = get_neighbor_indices(5)
    assert set(neighbors) == {0, 1, 2, 4, 6, 8, 9, 10}


path_extensions = [
    ([0, 5], [
                   [0, 5, 1], [0, 5, 2],
        [0, 5, 4],            [0, 5, 6],
        [0, 5, 8], [0, 5, 9], [0, 5, 10],
    ]),
    ([5, 0], [[5, 0, 1], [5, 0, 4]]),
    ([1, 5, 4, 0], []),
]


@pytest.mark.parametrize('path,expected_extensions', path_extensions)
def test_extend_path(path, expected_extensions):
    extensions = extend_path(path)
    assert sorted(extensions) == sorted(expected_extensions)
