"""Uniform-Cost Search.

UCS always expands the cell with the lowest cost so far (g). Because the
cheapest known cost always comes out of the queue first, the first time the
goal comes out, no cheaper way to reach it can exist. That is why UCS finds
the CHEAPEST path (not just the one with the fewest moves).
"""
import heapq
import itertools
import time

from core import find_start_goal, neighbors, step_cost, reconstruct_path, make_result


def ucs(grid):
    t0 = time.perf_counter()  # start the timer
    start, goal = find_start_goal(grid)

    counter = itertools.count()  # tie-breaker: goes up by 1 on every push
    best_g = {start: 0}          # cheapest cost found so far to reach each cell (S costs 0)
    parents = {start: None}      # which cell we came from (used to rebuild the path)
    # each queue entry is (priority, counter, g, position); for UCS priority = g
    queue = [(0, next(counter), 0, start)]
    expanded = 0       # number of non-stale entries taken out of the queue
    max_frontier = 1   # biggest the queue ever got

    while queue:
        _, _, g, pos = heapq.heappop(queue)  # take out the cheapest entry

        if g > best_g[pos]:
            continue  # stale entry: a cheaper route to this cell was found later, skip it

        expanded += 1

        if pos == goal:  # goal test happens when we take G OUT, not when we put it in
            path = reconstruct_path(parents, goal)
            elapsed = time.perf_counter() - t0
            return make_result("UCS", path, g, expanded, max_frontier, elapsed)

        for nb in neighbors(grid, pos):
            new_g = g + step_cost(grid, nb)  # cost so far + cost of entering the neighbour
            if new_g < best_g.get(nb, float("inf")):  # strictly cheaper than anything known
                best_g[nb] = new_g
                parents[nb] = pos
                heapq.heappush(queue, (new_g, next(counter), new_g, nb))
                max_frontier = max(max_frontier, len(queue))

    # queue ran empty and we never took G out: there is no path
    elapsed = time.perf_counter() - t0
    return make_result("UCS", None, None, expanded, max_frontier, elapsed)