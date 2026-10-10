"""Program entry point."""
from ucs import ucs
from astar import astar
from display import print_result

MAP_A = [
    "S..#....",
    "##.#.##.",
    "....~~..",
    ".####.#.",
    "...~..#G"
]

MAP_B = [
    "S~~~~~~~G",
    ".#######.",
    ".........",
    ".#.#.#.#.",
    "........."
]

MAP_C = [
    "S..#....",
    ".#.#.##.",
    "...#..#.",
    ".###.##.",
    "....#..G"
]

# Change this line to MAP_B or MAP_C to run on another map
GRID = MAP_A

if __name__ == "__main__":
    # run both searches on the chosen map and print each result
    for search in (ucs, astar):
        result = search(GRID)
        print_result(result, GRID)
        print()   # blank line between the two results