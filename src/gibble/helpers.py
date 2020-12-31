def make_grid_array(flat_grid):
    grid = [[None] * 4 for _ in range(4)]
    for i, letter in enumerate(flat_grid):
        grid[i // 4][i % 4] = letter
    return grid
