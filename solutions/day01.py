# %% [markdown]
# # Advent of Code 2025 - Day 1: Secret Entrance
#
# **Problem Summary:**
# We need to open a safe with a circular dial (numbered 0-99) by following rotation commands.
# The dial starts at position 50 and responds to:
# - L (left/lower numbers) - decrease the position
# - R (right/higher numbers) - increase the position
#
# The dial wraps around: left from 0 goes to 99; right from 99 goes to 0.
#
# **Goal:** Count how many times the dial lands exactly on 0 after completing each rotation.
#
# **Approach:**
# 1. Parse each command to extract direction (L/R) and distance (number of clicks)
# 2. Starting at position 50, apply each rotation
# 3. Track wrapping behavior (0-99 circular)
# 4. Count each time we land exactly on 0

# %%
# Load input data (only when running as script, not when importing for tests)
import os

if os.path.exists("../resources/inputs/day01.txt"):
    with open("../resources/inputs/day01.txt", "r") as f:
        puzzle_input = f.read().strip()
elif os.path.exists("resources/inputs/day01.txt"):
    with open("resources/inputs/day01.txt", "r") as f:
        puzzle_input = f.read().strip()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Part 1: Count Times Dial Lands on Zero
#
# **Algorithm:**
# 1. Start at position 50
# 2. For each rotation command:
#    - Parse direction (L or R) and distance (number)
#    - Apply rotation with modulo 100 for wrapping
#    - If position == 0, increment counter
# 3. Return the count
#
# **Example walkthrough:**
# - Start: 50
# - L68: 50 - 68 = -18 → 82 (mod 100)
# - L30: 82 - 30 = 52
# - R48: 52 + 48 = 100 → 0 (mod 100) ✓ (count = 1)
# - L5: 0 - 5 = -5 → 95 (mod 100)
# - R60: 95 + 60 = 155 → 55 (mod 100)
# - L55: 55 - 55 = 0 ✓ (count = 2)
# - L1: 0 - 1 = -1 → 99 (mod 100)
# - L99: 99 - 99 = 0 ✓ (count = 3)
# - R14: 0 + 14 = 14
# - L82: 14 - 82 = -68 → 32 (mod 100)
#
# Total: 3 times landing on 0

# %%
# Part 1: Example data
example_input_1 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


# %%
# Part 1: Solution function
def solve_part1(data):
    """
    Count how many times the dial lands on 0 after rotations.

    Args:
        data: Input data as string with rotation commands (e.g., "L68\nR30")

    Returns:
        Number of times dial lands on position 0
    """
    position = 50  # Starting position
    count = 0  # Count of times landing on 0

    # Process each rotation command
    for line in data.strip().split("\n"):
        direction = line[0]  # 'L' or 'R'
        distance = int(line[1:])  # Number of clicks

        # Apply rotation
        if direction == "L":
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100

        # Check if we landed on 0
        if position == 0:
            count += 1

    return count


# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
# Expected: 3

# %%
# Part 1: Solve with real input
result_part1 = solve_part1(puzzle_input)
print(f"Part 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: Count All Clicks Through Zero
#
# **New requirement:** Count EVERY time the dial points at 0, including during rotations.
#
# **Key difference from Part 1:**
# - Part 1: Only counted when rotation ended on 0
# - Part 2: Count every click that passes through 0 during the rotation
#
# **Example cases:**
# - L68 from 50→82: Path is 50→49→...→1→0→99→...→82 (crosses 0 once)
# - R48 from 52→0: Path is 52→53→...→99→0 (crosses 0 once, lands on it)
# - R60 from 95→55: Path is 95→96→...→99→0→1→...→55 (crosses 0 once)

# %%
# Part 2: Example (same as Part 1)
example_input_2 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


# %%
# Part 2: Solution function
def solve_part2(data):
    """
    Count how many times the dial points at 0 during all rotations.
    This includes both ending on 0 and passing through 0 during rotation.

    Args:
        data: Input data as string with rotation commands (e.g., "L68\nR30")

    Returns:
        Total number of times dial points at 0 (including during rotations)
    """
    position = 50  # Starting position
    count = 0  # Count of times pointing at 0

    # Process each rotation command
    for line in data.strip().split("\n"):
        direction = line[0]  # 'L' or 'R'
        distance = int(line[1:])  # Number of clicks

        # Simulate each click to count every time we land on 0
        for i in range(1, distance + 1):
            if direction == "L":
                position = (position - 1) % 100
            else:  # direction == 'R'
                position = (position + 1) % 100

            if position == 0:
                count += 1

    return count


# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
# Expected: 6

# %%
# Part 2: Solve with real input
if puzzle_input:
    result_part2 = solve_part2(puzzle_input)
    print(f"Part 2 Answer: {result_part2}")
