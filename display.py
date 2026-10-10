"""Drawing and printing results (owner: Person 2)."""


def draw_path(grid, path):
    """Return a copy of the map with * on every cell of the path.

    S and G stay as they are, so we can still see where the robot
    starts and ends. The original grid is not changed and nothing is
    printed here. If path is None (no path found), the map comes back
    unchanged.
    """
    if path is None:
        path = []

    # strings can't be edited in Python, so turn each row into a list of letters
    rows = [list(row) for row in grid]

    for r, c in path:
        if rows[r][c] not in ("S", "G"):   # never cover the start or the goal
            rows[r][c] = "*"

    # turn each row back into a string
    return ["".join(row) for row in rows]


def print_result(result, grid):
    """Print one search result in the layout the team agreed on.

    result is the dictionary an algorithm returns (name, path, cost,
    expanded, max_frontier, time). grid is the map, used to draw the path.
    """
    print(f"=== {result['name']} ===")

    path = result["path"]
    if path is None:
        # no path: there is no cost or drawing to show
        print("No path found")
    else:
        print("Path:", path)
        print("Path length (moves):", len(path) - 1)   # moves = cells - 1
        print("Total cost:", result["cost"])

    # these are filled in even when no path exists
    print("Nodes expanded:", result["expanded"])
    print("Max frontier:", result["max_frontier"])
    print(f"Time: {result['time'] * 1000:.4f} ms")      # seconds -> milliseconds

    if path is not None:
        for row in draw_path(grid, path):               # the map with * on it
            print(row)