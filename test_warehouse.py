"""Tests for the warehouse robot project."""
import copy
import random
import unittest

from main import MAP_A, MAP_B, MAP_C
from core import find_start_goal, neighbors
from ucs import ucs
from astar import astar
from display import draw_path
from bfs import bfs

# own cost table, so the checker does not depend on step_cost from core.py
CHECK_COST = {".": 1, "~": 3, "G": 1}

PATH_A = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
          (2, 5), (2, 6), (2, 7), (3, 7), (4, 7)]
PATH_B = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
          (2, 5), (2, 6), (2, 7), (2, 8), (1, 8), (0, 8)]


def find_cell(grid, letter):
    # looks for S or G on its own, without using find_start_goal
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == letter:
                return (r, c)
    return None


def check_path(grid, path):
    """checks a path and returns its cost (S is not counted)"""
    start = find_cell(grid, "S")
    goal = find_cell(grid, "G")
    if path[0] != start:
        raise AssertionError("path does not start at S")
    if path[-1] != goal:
        raise AssertionError("path does not end at G")

    total = 0
    for i in range(1, len(path)):
        r, c = path[i]
        pr, pc = path[i - 1]
        # exactly one step up, down, left or right
        if abs(r - pr) + abs(c - pc) != 1:
            raise AssertionError("bad step from " + str(path[i - 1]) + " to " + str(path[i]))
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[r]):
            raise AssertionError("path leaves the grid at " + str(path[i]))
        cell = grid[r][c]
        if cell == "#":
            raise AssertionError("path goes through a wall at " + str(path[i]))
        if cell == "S":
            raise AssertionError("path goes back into S")
        total += CHECK_COST[cell]
    return total


class TestCore(unittest.TestCase):
    def test_find_start_goal(self):
        self.assertEqual(find_start_goal(MAP_A), ((0, 0), (4, 7)))
        self.assertEqual(find_start_goal(MAP_B), ((0, 0), (0, 8)))
        self.assertEqual(find_start_goal(MAP_C), ((0, 0), (4, 7)))

    def test_neighbors_corner(self):
        # top left corner: up and left are outside, down is a wall
        self.assertEqual(neighbors(MAP_A, (0, 0)), [(0, 1)])

    def test_neighbors_order_next_to_wall(self):
        # (2,2) in MAP_A: down is a wall, the rest must be Up, Left, Right
        self.assertEqual(neighbors(MAP_A, (2, 2)), [(1, 2), (2, 1), (2, 3)])
        # (1,2): walls on the left and right
        self.assertEqual(neighbors(MAP_A, (1, 2)), [(0, 2), (2, 2)])

    def test_no_start_raises(self):
        with self.assertRaises(ValueError):
            find_start_goal(["...", "..G"])

    def test_no_goal_raises(self):
        with self.assertRaises(ValueError):
            find_start_goal(["S..", "..."])

    def test_two_starts_raises(self):
        with self.assertRaises(ValueError):
            find_start_goal(["S.S", "..G"])


class TestGolden(unittest.TestCase):
    def check_a(self, result):
        self.assertEqual(result["cost"], 15)
        self.assertEqual(len(result["path"]) - 1, 11)
        self.assertEqual(result["path"], PATH_A)

    def check_b(self, result):
        self.assertEqual(result["cost"], 12)
        self.assertEqual(len(result["path"]) - 1, 12)
        self.assertEqual(result["path"], PATH_B)

    def check_c(self, result):
        self.assertIsNone(result["path"])
        self.assertIsNone(result["cost"])
        self.assertEqual(result["expanded"], 13)

    def test_ucs_map_a(self):
        self.check_a(ucs(MAP_A))

    def test_ucs_map_b(self):
        self.check_b(ucs(MAP_B))

    def test_ucs_map_c(self):
        self.check_c(ucs(MAP_C))

    def test_astar_map_a(self):
        self.check_a(astar(MAP_A))

    def test_astar_map_b(self):
        self.check_b(astar(MAP_B))

    def test_astar_map_c(self):
        self.check_c(astar(MAP_C))

    def test_result_keys(self):
        keys = {"name", "path", "cost", "expanded", "max_frontier", "time"}
        for search in (ucs, astar):
            self.assertEqual(set(search(MAP_A).keys()), keys)

    def test_names(self):
        self.assertEqual(ucs(MAP_A)["name"], "UCS")
        self.assertEqual(astar(MAP_A)["name"], "A*")

    def test_draw_path_map_a(self):
        drawn = draw_path(MAP_A, PATH_A)
        self.assertEqual(drawn, [
            "S**#....",
            "##*#.##.",
            "..******",
            ".####.#*",
            "...~..#G",
        ])


class TestConsistency(unittest.TestCase):
    maps = [("A", MAP_A), ("B", MAP_B), ("C", MAP_C)]

    def test_same_cost(self):
        for name, grid in self.maps:
            self.assertEqual(ucs(grid)["cost"], astar(grid)["cost"], "map " + name)

    def test_cost_matches_checker(self):
        for name, grid in self.maps:
            for search in (ucs, astar):
                result = search(grid)
                if result["path"] is not None:
                    self.assertEqual(result["cost"], check_path(grid, result["path"]),
                                     result["name"] + " on map " + name)

    def test_grid_not_changed(self):
        for name, grid in self.maps:
            for search in (ucs, astar, bfs):
                before = copy.deepcopy(grid)
                search(grid)
                self.assertEqual(grid, before)

    def test_astar_not_more_nodes(self):
        for name, grid in self.maps:
            self.assertLessEqual(astar(grid)["expanded"], ucs(grid)["expanded"], "map " + name)


class TestRandom(unittest.TestCase):
    def test_random_grids(self):
        rng = random.Random(42)
        for i in range(200):
            rows = []
            for r in range(6):
                row = ""
                for c in range(6):
                    x = rng.random()
                    if x < 0.25:
                        row += "#"
                    elif x < 0.45:
                        row += "~"
                    else:
                        row += "."
                rows.append(row)
            # S top left, G bottom right
            rows[0] = "S" + rows[0][1:]
            rows[5] = rows[5][:5] + "G"

            u = ucs(rows)
            a = astar(rows)
            if u["path"] is None or a["path"] is None:
                self.assertIsNone(u["path"], "grid " + str(i))
                self.assertIsNone(a["path"], "grid " + str(i))
            else:
                self.assertEqual(u["cost"], a["cost"], "grid " + str(i))
                self.assertEqual(check_path(rows, u["path"]), u["cost"])
                self.assertEqual(check_path(rows, a["path"]), a["cost"])


class TestEdgeCases(unittest.TestCase):
    def test_s_next_to_g(self):
        for search in (ucs, astar):
            result = search(["SG"])
            self.assertEqual(result["cost"], 1)
            self.assertEqual(len(result["path"]), 2)

    def test_cheap_way_is_longer(self):
        grid = ["S~~G",
                "...."]
        for search in (ucs, astar):
            result = search(grid)
            # straight along the top is 3 moves but costs 7, going round costs 5
            self.assertEqual(result["cost"], 5)
            self.assertEqual(len(result["path"]) - 1, 5)
            self.assertEqual(check_path(grid, result["path"]), 5)

    def test_one_row(self):
        for search in (ucs, astar):
            result = search(["S..G"])
            self.assertEqual(result["cost"], 3)
            self.assertEqual(len(result["path"]) - 1, 3)

    def test_one_row_blocked(self):
        for search in (ucs, astar):
            result = search(["S#G"])
            self.assertIsNone(result["path"])
            self.assertIsNone(result["cost"])


class TestBfs(unittest.TestCase):
    def test_bfs_trap_on_map_b(self):
        result = bfs(MAP_B)
        self.assertEqual(len(result["path"]) - 1, 8)
        self.assertEqual(result["cost"], 22)
        self.assertEqual(check_path(MAP_B, result["path"]), 22)

    def test_bfs_no_path_map_c(self):
        result = bfs(MAP_C)
        self.assertIsNone(result["path"])
        self.assertEqual(result["expanded"], 13)


if __name__ == "__main__":
    unittest.main()
