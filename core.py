"""Shared helpers used by every search algorithm."""

# The four moves as (row change, column change): Up, Down, Left, Right
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_start_goal(grid):
    """the grid is a list of strings, one per row. this function returns the positions of S and G."""
    start = None
    goal = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                if start is not None:
                    raise ValueError("Map has more than one S")
                start = (r, c)
            elif cell == "G":
                if goal is not None:
                    raise ValueError("Map has more than one G")
                goal = (r, c)
    if start is None:
        raise ValueError("Map has no S")
    if goal is None:
        raise ValueError("Map has no G")
    return start, goal


def neighbors(grid, pos):
    """given a cell, returns the cells the robot can step into, in the order Up,Down,Left,Right."""
    # NOTE: . means normal floor (cost 1), # means wall, ~ means a rough floor (cost 3)
    available_neighbors = []
    for move in MOVES:
        new_r = pos[0] + move[0]
        new_c = pos[1] + move[1] 
        if new_r < 0 or new_r >= len(grid):
            # row is outside the grid
            continue 
        if new_c < 0 or new_c >= len(grid[0]):  
            # column is outside the grid
            continue
        if grid[new_r][new_c] == "#":
            # wall, can't step into it
            continue
        available_neighbors.append((new_r, new_c))
    return available_neighbors



def step_cost(grid, pos):
    """cost of ENTERING the cell at pos: 3 for rough floor (~), otherwise 1 (. and G)"""
    if grid[pos[0]][pos[1]] == "~":
        return 3
    return 1


def reconstruct_path(parents, goal):
    """follow the parent links back from the goal to the start, then reverse so the path reads S to G."""
    path = []
    current = goal
    while current is not None:  # the start cell has parent None, which stops the loop
        path.append(current)
        current = parents[current]
    path.reverse()
    return path


def make_result(name, path, cost, expanded, max_frontier, time):
    """build the result dictionary every algorithm returns."""
    return {
        "name": name,
        "path": path,
        "cost": cost,
        "expanded": expanded,
        "max_frontier": max_frontier,
        "time": time,
    }