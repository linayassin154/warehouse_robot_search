"""Benchmark table for UCS and A* on MAP_A, MAP_B and MAP_C.

Run with: python benchmark.py
It prints the table and also writes it to results.md
"""
from main import MAP_A, MAP_B, MAP_C
from ucs import ucs
from astar import astar
from bfs import bfs

WARMUP = 10

DEFINITIONS = """Definitions

- Path length (moves): number of moves, which is the number of cells in the path minus 1.
- Path cost: sum of the cost of every cell entered (. = 1, G = 1, ~ = 3). S is not counted.
- Nodes expanded: number of non-stale nodes taken out of the queue, including the one for G.
- Max frontier: largest queue size seen after any push. It includes stale entries.
- Avg time (ms): average of the time each search reports, over the number of runs, in milliseconds.
"""


def run_one(search, grid, n_runs):
    # warm-up calls, not recorded
    for _ in range(WARMUP):
        search(grid)

    first = search(grid)
    total_time = first["time"]
    for _ in range(n_runs - 1):
        r = search(grid)
        # these must never change between calls
        if (r["expanded"] != first["expanded"]
                or r["cost"] != first["cost"]
                or r["max_frontier"] != first["max_frontier"]):
            raise RuntimeError("results changed between runs for " + first["name"])
        total_time += r["time"]

    avg_ms = total_time / n_runs * 1000
    if first["path"] is None:
        length = "N/A"
        cost = "N/A"
    else:
        length = len(first["path"]) - 1
        cost = first["cost"]
    return {
        "map": None,
        "algorithm": first["name"],
        "length": length,
        "cost": cost,
        "expanded": first["expanded"],
        "max_frontier": first["max_frontier"],
        "avg_ms": avg_ms,
    }


def run_all(n_runs=1000):
    maps = [("MAP_A", MAP_A), ("MAP_B", MAP_B), ("MAP_C", MAP_C)]
    rows = []
    for map_name, grid in maps:
        for search in (ucs, astar):
            row = run_one(search, grid, n_runs)
            row["map"] = map_name
            rows.append(row)
    return rows


def make_table(rows):
    lines = []
    lines.append("| Map | Algorithm | Path length (moves) | Path cost | Nodes expanded | Max frontier | Avg time (ms) |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append("| {} | {} | {} | {} | {} | {} | {:.4f} |".format(
            r["map"], r["algorithm"], r["length"], r["cost"],
            r["expanded"], r["max_frontier"], r["avg_ms"]))
    return "\n".join(lines)


def make_notes(rows):
    notes = []
    for map_name in ("MAP_A", "MAP_B", "MAP_C"):
        u = [r for r in rows if r["map"] == map_name and r["algorithm"] == "UCS"][0]
        a = [r for r in rows if r["map"] == map_name and r["algorithm"] == "A*"][0]
        if u["expanded"] == a["expanded"]:
            notes.append("- {}: UCS and A* expanded the same number of nodes ({}).".format(map_name, u["expanded"]))
        elif a["expanded"] < u["expanded"]:
            notes.append("- {}: A* expanded fewer nodes than UCS ({} vs {}).".format(map_name, a["expanded"], u["expanded"]))
        else:
            notes.append("- {}: A* expanded more nodes than UCS ({} vs {}).".format(map_name, a["expanded"], u["expanded"]))
        if u["cost"] != a["cost"]:
            notes.append("- {}: the costs are different, something is wrong.".format(map_name))
    return "\n".join(notes)


def print_bfs_extra():
    print()
    print("EXTRA (not part of the main table): BFS")
    for map_name, grid in (("MAP_A", MAP_A), ("MAP_B", MAP_B), ("MAP_C", MAP_C)):
        r = bfs(grid)
        if r["path"] is None:
            print(map_name, "-> No path found, expanded", r["expanded"])
        else:
            print(map_name, "-> moves", len(r["path"]) - 1, "cost", r["cost"],
                  "expanded", r["expanded"], "max frontier", r["max_frontier"])


if __name__ == "__main__":
    n_runs = 1000
    rows = run_all(n_runs)
    table = make_table(rows)
    notes = make_notes(rows)

    text = DEFINITIONS + "\nResults (" + str(n_runs) + " runs per row, after " + str(WARMUP) + " warm-up calls)\n\n" + table + "\n\nNotes\n\n" + notes + "\n"

    print(text)
    with open("results.md", "w", encoding="utf-8") as f:
        f.write(text)

    print_bfs_extra()
