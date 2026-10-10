"""
BFS expands the cells with the fewest moves first and ignores the floor costs.
That is why it falls into the trap on MAP_B: it finds the path with the fewest
moves, but not the cheapest one.
"""
import time
from collections import deque

from core import find_start_goal, neighbors, step_cost, reconstruct_path, make_result


def bfs(grid):
    t0 = time.perf_counter()
    start, goal = find_start_goal(grid)

    # queue entries are (position, g), the same info the other searches keep
    queue = deque([(start, 0)])
    parents = {start: None}   # also works as the "already seen" set
    expanded = 0
    max_frontier = 1

    while queue:
        pos, g = queue.popleft()
        expanded += 1

        # goal test when taken OUT of the queue, same as UCS and A*
        if pos == goal:
            path = reconstruct_path(parents, goal)
            elapsed = time.perf_counter() - t0
            return make_result("BFS (extra)", path, g, expanded, max_frontier, elapsed)

        for nb in neighbors(grid, pos):
            if nb not in parents:
                parents[nb] = pos
                # the cost is only added up, bfs does not use it to choose
                queue.append((nb, g + step_cost(grid, nb)))
                max_frontier = max(max_frontier, len(queue))

    elapsed = time.perf_counter() - t0
    return make_result("BFS (extra)", None, None, expanded, max_frontier, elapsed)
