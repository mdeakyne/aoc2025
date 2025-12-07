# %% [markdown]
# # Advent of Code 2025 - Day 4: Printing Department
#
# **Problem Summary:**
# Grid with paper rolls (@) and empty spaces (.).
# A forklift can access a roll if it has fewer than 4 adjacent paper rolls.
# Count how many rolls are accessible.
#
# **Approach:**
# - Use a Grid class to encapsulate the paper roll map
# - Count neighbors in 8 directions (N, NE, E, SE, S, SW, W, NW)
# - A roll is accessible if it has < 4 neighboring rolls

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day04.txt"):
    with open("../resources/inputs/day04.txt", "r") as f:
        puzzle_input = f.read().strip()
elif os.path.exists("resources/inputs/day04.txt"):
    with open("resources/inputs/day04.txt", "r") as f:
        puzzle_input = f.read().strip()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Part 1: Count Accessible Paper Rolls
#
# **Algorithm:**
# 1. Parse grid into 2D array
# 2. For each cell with '@':
#    - Count adjacent '@' symbols (8 directions)
#    - If count < 4, roll is accessible
# 3. Return total count of accessible rolls

# %%
# Part 1: Example data
example_input_1 = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


# %%
# Grid class to encapsulate the paper roll map
class Grid:
    """Represents a grid of paper rolls and empty spaces."""

    # 8-directional neighbor offsets: N, NE, E, SE, S, SW, W, NW
    DIRECTIONS = [
        (-1, 0),  # N
        (-1, 1),  # NE
        (0, 1),  # E
        (1, 1),  # SE
        (1, 0),  # S
        (1, -1),  # SW
        (0, -1),  # W
        (-1, -1),  # NW
    ]

    def __init__(self, data: str):
        """
        Parse the input into a 2D grid.

        Args:
            data: Input string with grid layout
        """
        self.grid = [list(line) for line in data.strip().split("\n")]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0

    def count_neighbors(self, row: int, col: int) -> int:
        """
        Count the number of paper rolls ('@') in adjacent cells.

        Args:
            row: Row index
            col: Column index

        Returns:
            Count of adjacent paper rolls (0-8)
        """
        count = 0
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            # Check boundaries
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.grid[r][c] == "@":
                    count += 1
        return count

    def is_accessible(self, row: int, col: int) -> bool:
        """
        Check if a paper roll at the given position is accessible.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if the position has a paper roll with < 4 neighbors
        """
        # Must be a paper roll
        if self.grid[row][col] != "@":
            return False

        # Must have fewer than 4 neighbors
        neighbor_count = self.count_neighbors(row, col)
        return neighbor_count < 4

    def count_accessible_rolls(self) -> int:
        """
        Count the total number of accessible paper rolls.

        Returns:
            Number of accessible rolls
        """
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_accessible(row, col):
                    count += 1
        return count

    def visualize_accessible(self) -> str:
        """
        Create a visualization showing accessible rolls as 'x'.

        Returns:
            String representation with accessible rolls marked
        """
        result = []
        for row in range(self.rows):
            line = []
            for col in range(self.cols):
                if self.is_accessible(row, col):
                    line.append("x")
                else:
                    line.append(self.grid[row][col])
            result.append("".join(line))
        return "\n".join(result)

    def remove_accessible_rolls(self) -> int:
        """
        Remove all accessible paper rolls from the grid (replace with '.').

        Returns:
            Number of rolls removed
        """
        # First, find all accessible positions
        to_remove = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_accessible(row, col):
                    to_remove.append((row, col))

        # Then remove them all at once (to avoid affecting neighbor counts mid-removal)
        for row, col in to_remove:
            self.grid[row][col] = "."

        return len(to_remove)

    def remove_all_accessible_rolls(self) -> int:
        """
        Recursively remove accessible rolls until none remain.

        Returns:
            Total number of rolls removed across all iterations
        """
        total_removed = 0

        while True:
            removed = self.remove_accessible_rolls()
            if removed == 0:
                break
            total_removed += removed

        return total_removed


# %%
# Part 1: Solution function
def solve_part1(data):
    """
    Count accessible paper rolls in the grid.

    Args:
        data: Input data as string

    Returns:
        Number of accessible rolls
    """
    grid = Grid(data)
    return grid.count_accessible_rolls()


# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
print(f"Expected: 13")

# Show visualization
print("\nAccessible rolls marked with 'x':")
grid = Grid(example_input_1)
print(grid.visualize_accessible())

# %%
# Part 1: Solve with real input
if puzzle_input:
    result_part1 = solve_part1(puzzle_input)
    print(f"\nPart 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: Recursive Removal
#
# Now we need to remove accessible rolls iteratively:
# 1. Find and remove all accessible rolls (< 4 neighbors)
# 2. Repeat until no more can be removed
# 3. Count total rolls removed across all iterations
#
# The example shows: 13 + 12 + 7 + 5 + 2 + 1 + 1 + 1 + ... = total removed

# %%
# Part 2: Example data (same as Part 1)
example_input_2 = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


# %%
# Part 2: Solution function
def solve_part2(data):
    """
    Recursively remove all accessible paper rolls.

    Args:
        data: Input data as string

    Returns:
        Total number of rolls removed across all iterations
    """
    grid = Grid(data)
    return grid.remove_all_accessible_rolls()


# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
print(f"Expected: 43 (13+12+7+5+2+1+1+1+1 from the description)")

# %%
# Part 2: Solve with real input
if puzzle_input:
    result_part2 = solve_part2(puzzle_input)
    print(f"\nPart 2 Answer: {result_part2}")
