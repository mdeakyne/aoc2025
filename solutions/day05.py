# %% [markdown]
# # Advent of Code 2025 - Day 5: Cafeteria
#
# **Problem Summary:**
# Database has:
# 1. Fresh ingredient ID ranges (e.g., "3-5" means IDs 3, 4, 5 are fresh)
# 2. List of available ingredient IDs
# Count how many available IDs are fresh.
#
# **Approach:**
# - Parse ranges into sets using range()
# - Use set union to combine all fresh ID ranges
# - Count how many available IDs are in the fresh set (using `in` operator)

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day05.txt"):
    with open("../resources/inputs/day05.txt", "r") as f:
        puzzle_input = f.read().strip()
elif os.path.exists("resources/inputs/day05.txt"):
    with open("resources/inputs/day05.txt", "r") as f:
        puzzle_input = f.read().strip()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Part 1: Count Fresh Ingredients
#
# **Algorithm:**
# 1. Split input into ranges section and ingredient IDs section (separated by blank line)
# 2. Parse each range "start-end" into set(range(start, end+1))
# 3. Union all range sets to get complete fresh ingredient set
# 4. Count how many ingredient IDs are in the fresh set
#
# **Example:**
# - Ranges: 3-5, 10-14, 16-20, 12-18
# - Fresh set: {3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
# - Available IDs: [1, 5, 8, 11, 17, 32]
# - Fresh count: 3 (IDs 5, 11, 17)

# %%
# Part 1: Example data
example_input_1 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


# %%
# Part 1: Solution function
def solve_part1(data):
    """
    Count how many available ingredient IDs are fresh.

    Args:
        data: Input data as string (ranges, blank line, ingredient IDs)

    Returns:
        Number of fresh ingredients
    """
    # Split into ranges section and IDs section
    sections = data.strip().split("\n\n")
    ranges_section = sections[0]
    ids_section = sections[1]

    # Parse ranges into a list of (start, end) tuples
    # NOTE: Ranges can be HUGE (trillions), so we can't create sets
    fresh_ranges = []
    for line in ranges_section.strip().split("\n"):
        start, end = map(int, line.split("-"))
        fresh_ranges.append((start, end))

    # Parse ingredient IDs
    ingredient_ids = [int(line) for line in ids_section.strip().split("\n")]

    # Count how many are fresh by checking if they fall in any range
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        # Check if this ID falls within any fresh range
        for start, end in fresh_ranges:
            if start <= ingredient_id <= end:
                fresh_count += 1
                break  # Found a match, no need to check other ranges

    return fresh_count


# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
print(f"Expected: 3")

# Show which IDs are fresh
sections = example_input_1.strip().split("\n\n")
ranges_section = sections[0]
ids_section = sections[1]

fresh_ids = set()
for line in ranges_section.strip().split("\n"):
    start, end = map(int, line.split("-"))
    fresh_ids |= set(range(start, end + 1))

ingredient_ids = [int(line) for line in ids_section.strip().split("\n")]

print("\nIngredient breakdown:")
for ingredient_id in ingredient_ids:
    status = "fresh" if ingredient_id in fresh_ids else "spoiled"
    print(f"  ID {ingredient_id}: {status}")

# %%
# Part 1: Solve with real input
if puzzle_input:
    result_part1 = solve_part1(puzzle_input)
    print(f"\nPart 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: Count Total Unique Fresh IDs
#
# Now we need to count how many UNIQUE ingredient IDs are considered fresh
# across all ranges (ranges can overlap).
#
# **Strategy:**
# 1. Sort ranges by start position
# 2. Merge overlapping/adjacent ranges
# 3. Sum the lengths of merged ranges
#
# **Example:**
# - Ranges: 3-5, 10-14, 16-20, 12-18
# - Sorted: 3-5, 10-14, 12-18, 16-20
# - Merged: [3-5], [10-20] (12-18 and 16-20 merge with 10-14)
# - Count: (5-3+1) + (20-10+1) = 3 + 11 = 14

# %%
# Part 2: Example data (same as Part 1, but only need ranges)
example_input_2 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


# %%
# Part 2: Solution function
def solve_part2(data):
    """
    Count total unique ingredient IDs considered fresh across all ranges.

    Args:
        data: Input data as string (ranges, blank line, ingredient IDs)

    Returns:
        Total number of unique fresh ingredient IDs
    """
    # Split into ranges section (we don't need the IDs section)
    sections = data.strip().split("\n\n")
    ranges_section = sections[0]

    # Parse ranges into a list of (start, end) tuples
    ranges = []
    for line in ranges_section.strip().split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    # Sort ranges by start position
    ranges.sort()

    # Merge overlapping/adjacent ranges
    merged = []
    for start, end in ranges:
        if not merged:
            # First range
            merged.append([start, end])
        else:
            # Check if current range overlaps or is adjacent to the last merged range
            last_start, last_end = merged[-1]
            if start <= last_end + 1:
                # Overlap or adjacent - merge by extending the end
                merged[-1][1] = max(last_end, end)
            else:
                # No overlap - start a new merged range
                merged.append([start, end])

    # Count total IDs across all merged ranges
    total_count = 0
    for start, end in merged:
        total_count += end - start + 1

    return total_count


# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
print(f"Expected: 14")

# Show merged ranges
sections = example_input_2.strip().split("\n\n")
ranges_section = sections[0]
ranges = []
for line in ranges_section.strip().split("\n"):
    start, end = map(int, line.split("-"))
    ranges.append((start, end))
ranges.sort()

merged = []
for start, end in ranges:
    if not merged:
        merged.append([start, end])
    else:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

print(f"\nOriginal ranges (sorted): {ranges}")
print(f"Merged ranges: {merged}")
print(f"Range lengths: {[end - start + 1 for start, end in merged]}")

# %%
# Part 2: Solve with real input
if puzzle_input:
    result_part2 = solve_part2(puzzle_input)
    print(f"\nPart 2 Answer: {result_part2}")
