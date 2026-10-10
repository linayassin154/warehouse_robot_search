"""A* search with Manhattan distance 

A* works like UCS, but it also guesses how far each cell is from G,
so it tries the cells that look closer to G first.
"""
import heapq
import time

from core import find_start_goal, neighbors, step_cost, reconstruct_path, make_result


def manhattan(pos, goal):
    """Straight-line distance on a grid: rows apart + columns apart.

    The robot moves one cell at a time, so with no walls the fewest
    moves from pos to goal is exactly this number. Every move costs at
    least 1, so the real cost can never be smaller than this guess.
    That is why A* still finds the cheapest path with it.

    """
    row_gap = abs(pos[0] - goal[0])   # how many rows apart
    col_gap = abs(pos[1] - goal[1])   # how many columns apart
    return row_gap + col_gap


def astar(grid):
    """Find the cheapest path from S to G using A*.

    Same as UCS, but the queue is ordered by g + manhattan instead of g.
    g is the real cost so far. The Manhattan part is only a guess that
    helps us try cells closer to G first. The cost we return is always g.
    """
    start_time = time.perf_counter()
    start, goal = find_start_goal(grid)   # S and G are found by scanning the grid

    counter = 0                  # goes up on every push, breaks ties in the queue
    best_cost = {start: 0}       # cheapest cost found so far for each cell (S costs 0)
    parents = {start: None}      # where each cell was reached from
    expanded = 0                 # cells we really processed
    max_frontier = 1             # biggest queue size seen

    # each queue item is (priority, counter, g, position)
    queue = [(manhattan(start, goal), counter, 0, start)]

    while queue:
        _, _, g, pos = heapq.heappop(queue)

        # we already found a cheaper way to this cell, so this item is old
        if g > best_cost[pos]:
            continue

        expanded += 1

        # check for the goal when taking it OUT of the queue, not when adding it
        if pos == goal:
            path = reconstruct_path(parents, goal)
            elapsed = time.perf_counter() - start_time
            return make_result("A*", path, g, expanded, max_frontier, elapsed)

        for next_pos in neighbors(grid, pos):
            new_g = g + step_cost(grid, next_pos)

            # only keep it if it's a new cell or a cheaper way to a known one
            if next_pos not in best_cost or new_g < best_cost[next_pos]:
                best_cost[next_pos] = new_g
                parents[next_pos] = pos
                counter += 1
                priority = new_g + manhattan(next_pos, goal)
                heapq.heappush(queue, (priority, counter, new_g, next_pos))
                max_frontier = max(max_frontier, len(queue))

    # queue ran out and we never reached G, so there is no path
    elapsed = time.perf_counter() - start_time
    return make_result("A*", None, None, expanded, max_frontier, elapsed)