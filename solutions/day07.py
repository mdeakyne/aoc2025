# %% [markdown]
# # Advent of Code 2025 - Day 7: Laboratories
#
# **Problem Summary:**
# Tachyon beam enters manifold at position S and travels downward.
# When beam hits a splitter (^), it stops and creates two new beams (left and right).
# Beams pass through empty space (.) and exit at bottom or edges.
#
# **Part 1:** Count total number of unique splitters hit.
# **Part 2:** Count total timelines (many-worlds interpretation - each split creates 2 universes).
#
# **Approach:**
# - Part 1: Recursive search with memoization to track visited splitters
# - Part 2: Recursive search counting timeline multiplier from each position

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day07.txt"):
    with open("../resources/inputs/day07.txt", "r") as f:
        puzzle_input = f.read()
elif os.path.exists("resources/inputs/day07.txt"):
    with open("resources/inputs/day07.txt", "r") as f:
        puzzle_input = f.read()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Grid Class
#
# Manages the tachyon manifold grid and beam traversal logic.
# - `count_splits()`: Part 1 - count unique splitters with deduplication
# - `count_timelines()`: Part 2 - count total universes with memoization


# %%
class Grid:
    def __init__(self, lines):
        self.grid = [list(line) for line in lines]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
        self.split_splitters = set()  # Track unique splitters that have been hit

    def find_start(self):
        """Find the S position and return its column index."""
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == "S":
                    return col
        return None

    def count_splits(self, start_row, col):
        """
        Count beam splits recursively.
        Search straight down from start_row in this column.
        If splitter (^) found, count it and recursively check left and right beams.
        Track unique splitters to avoid double-counting when beams converge.
        """
        # Bounds check
        if col < 0 or col >= self.width:
            return 0

        # Search down from start_row in this column
        for row in range(start_row, self.height):
            if self.grid[row][col] == "^":
                # Found a splitter! Check if we've already split it
                if (row, col) in self.split_splitters:
                    return 0

                # Mark this splitter as split
                self.split_splitters.add((row, col))

                # Count this split plus recursive splits from left and right
                left_splits = self.count_splits(row, col - 1)
                right_splits = self.count_splits(row, col + 1)
                return 1 + left_splits + right_splits

        # No splitter found in this column below start_row
        return 0

    def count_timelines(self, start_row, col, memo):
        """
        Count total timelines (universes) from this position.
        Uses memoization to cache results for (start_row, col) positions.

        Returns: Number of timelines that emerge from a beam starting at this position.
        - If no splitter: 1 timeline (beam exits)
        - If splitter at row R: left_timelines + right_timelines
        """
        # Bounds check - beam exits manifold
        if col < 0 or col >= self.width:
            return 1  # This timeline completes

        # Check memo
        if (start_row, col) in memo:
            return memo[(start_row, col)]

        # Search down from start_row in this column
        for row in range(start_row, self.height):
            if self.grid[row][col] == "^":
                # Found a splitter! Timeline splits into left and right
                left_timelines = self.count_timelines(row, col - 1, memo)
                right_timelines = self.count_timelines(row, col + 1, memo)
                result = left_timelines + right_timelines
                memo[(start_row, col)] = result
                return result

        # No splitter found - beam exits at bottom
        memo[(start_row, col)] = 1
        return 1


# %% [markdown]
# ## Part 1: Count Unique Splitters
#
# **Algorithm:**
# 1. Start beam at column S, row 0
# 2. Search downward for splitter (^)
# 3. When found, recursively search left (col-1) and right (col+1) from that row
# 4. Track visited splitters to avoid double-counting when beams converge
# 5. Return total count of unique splitters hit


# %%
def solve_part1(data):
    """Count how many times the beam is split."""
    lines = [line for line in data.split("\n") if line]

    grid = Grid(lines)
    start_col = grid.find_start()

    if start_col is None:
        return 0

    # Start searching from row 0 at the S column
    total_splits = grid.count_splits(0, start_col)

    return total_splits


# %%
# Part 1: Example
example_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

example_result = solve_part1(example_input)
print(f"Part 1 Example: {example_result}")
print(f"Expected: 21")

# %%
# Part 1: Solution
part1_answer = solve_part1(puzzle_input)
print(f"Part 1 Answer: {part1_answer}")

# %% [markdown]
# ## Part 2: Count Total Timelines (Many-Worlds Interpretation)
#
# **Algorithm:**
# 1. Each splitter creates 2 universes (left and right paths)
# 2. Count total universes by tracking timeline multiplier from each position
# 3. Use memoization: cache (start_row, col) -> timeline_count
# 4. When beam exits (bounds or bottom): contributes 1 timeline
# 5. When beam hits splitter: contributes left_timelines + right_timelines


# %%
def solve_part2(data):
    """Count total timelines (many-worlds interpretation)."""
    lines = [line for line in data.split("\n") if line]

    grid = Grid(lines)
    start_col = grid.find_start()

    if start_col is None:
        return 0

    # Start with 1 timeline at row 0, S column
    memo = {}
    total_timelines = grid.count_timelines(0, start_col, memo)

    return total_timelines


# %%
# Part 2: Example
example_result_p2 = solve_part2(example_input)
print(f"Part 2 Example: {example_result_p2}")
print(f"Expected: 40")

# %%
# Part 2: Solution
part2_answer = solve_part2(puzzle_input)
print(f"Part 2 Answer: {part2_answer}")
