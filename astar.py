"""A* search with Manhattan distance."""


def manhattan(pos, goal):
    """Straight-line distance on a grid: rows apart + columns apart.

    The robot moves one cell at a time, so with no walls the fewest
    moves from pos to goal is exactly this number. Every move costs at
    least 1, so the real cost can never be smaller than this guess.
    That is why A* still finds the cheapest path with it.
    Example: (0, 0) to (4, 7) -> 4 + 7 = 11.
    """
    row_gap = abs(pos[0] - goal[0])   # how many rows apart
    col_gap = abs(pos[1] - goal[1])   # how many columns apart
    return row_gap + col_gap


def astar(grid):
    raise NotImplementedError