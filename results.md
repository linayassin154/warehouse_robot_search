Definitions

- Path length (moves): number of moves, which is the number of cells in the path minus 1.
- Path cost: sum of the cost of every cell entered (. = 1, G = 1, ~ = 3). S is not counted.
- Nodes expanded: number of non-stale nodes taken out of the queue, including the one for G.
- Max frontier: largest queue size seen after any push. It includes stale entries.
- Avg time (ms): average of the time each search reports, over the number of runs, in milliseconds.

Results (1000 runs per row, after 10 warm-up calls)

| Map | Algorithm | Path length (moves) | Path cost | Nodes expanded | Max frontier | Avg time (ms) |
|---|---|---|---|---|---|---|
| MAP_A | UCS | 11 | 15 | 28 | 4 | 0.0410 |
| MAP_A | A* | 11 | 15 | 21 | 5 | 0.0304 |
| MAP_B | UCS | 12 | 12 | 31 | 4 | 0.0466 |
| MAP_B | A* | 12 | 12 | 15 | 7 | 0.0237 |
| MAP_C | UCS | N/A | N/A | 13 | 3 | 0.0198 |
| MAP_C | A* | N/A | N/A | 13 | 3 | 0.0184 |

Notes

- MAP_A: A* expanded fewer nodes than UCS (21 vs 28).
- MAP_B: A* expanded fewer nodes than UCS (15 vs 31).
- MAP_C: UCS and A* expanded the same number of nodes (13).
