"""Shared helpers used by every search algorithm (owner: Person 1)."""

# The four moves as (row change, column change): Up, Down, Left, Right
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_start_goal(grid):
    raise NotImplementedError


def neighbors(grid, pos):
    raise NotImplementedError


def step_cost(grid, pos):
    raise NotImplementedError


def reconstruct_path(parents, goal):
    raise NotImplementedError


def make_result(name, path, cost, expanded, max_frontier, time):
    raise NotImplementedError