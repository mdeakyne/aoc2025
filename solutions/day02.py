# %% [markdown]
# # Advent of Code 2025 - Day 2: Gift Shop
#
# **Problem Summary:**
# We need to identify invalid product IDs in the gift shop database.
# An invalid ID is one where the number is made of some sequence of digits repeated exactly twice.
#
# **Examples of invalid IDs:**
# - 11 (1 repeated twice)
# - 6464 (64 repeated twice)
# - 123123 (123 repeated twice)
# - 1188511885 (118851 repeated twice)
#
# **Valid IDs (not patterns repeated twice):**
# - 101 (not 10 repeated, and not 1 repeated - would need to be 1010 or 11)
# - 446443 (not a clean repeat)
#
# **Goal:** Sum all invalid IDs found within the given ranges.
#
# **Approach:**
# 1. Parse comma-separated ranges (e.g., "11-22,95-115")
# 2. For each range, check each number to see if it's invalid
# 3. A number is invalid if:
#    - It has an even number of digits
#    - The first half equals the second half
# 4. Sum all invalid IDs

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day02.txt"):
    with open("../resources/inputs/day02.txt", "r") as f:
        puzzle_input = f.read().strip()
elif os.path.exists("resources/inputs/day02.txt"):
    with open("resources/inputs/day02.txt", "r") as f:
        puzzle_input = f.read().strip()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Part 1: Find Invalid Product IDs
#
# **Algorithm:**
# 1. Parse ranges from comma-separated input
# 2. For each range (start-end):
#    - Check each number in the range
#    - Determine if it's invalid (pattern repeated twice)
# 3. Sum all invalid IDs
#
# **Helper function: is_invalid_id(num)**
# - Convert number to string
# - Check if length is even
# - Split in half and compare
#
# **Example walkthrough:**
# - 11-22: Check 11,12,13,...,22 → Invalid: 11, 22 → Sum: 33
# - 95-115: Check 95-115 → Invalid: 99 → Sum: 99
# - 998-1012: Check 998-1012 → Invalid: 1010 → Sum: 1010

# %%
# Part 1: Example data
example_input_1 = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


# %%
def is_invalid_id(num):
    """
    Check if a number is an invalid ID (pattern repeated exactly twice).

    Args:
        num: Integer to check

    Returns:
        True if the number is a pattern repeated twice, False otherwise
    """
    s = str(num)
    length = len(s)

    # Must have even number of digits to split in half
    if length % 2 != 0:
        return False

    # Split in half and compare
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]

    return first_half == second_half


# %%
# Part 1: Solution function
def solve_part1(data):
    """
    Find and sum all invalid product IDs in the given ranges.

    Args:
        data: Input data as string with comma-separated ranges (e.g., "11-22,95-115")

    Returns:
        Sum of all invalid product IDs
    """
    # Parse ranges
    ranges_str = data.strip().split(",")

    total = 0

    for range_str in ranges_str:
        # Parse start and end of range
        start, end = map(int, range_str.split("-"))

        # Check each number in the range
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num

    return total


# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
# Expected: 1227775554

# %%
# Part 1: Solve with real input
if puzzle_input:
    result_part1 = solve_part1(puzzle_input)
    print(f"Part 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: Find Invalid Product IDs (Repeated At Least Twice)
#
# **New Rule:** An ID is invalid if it's made of some sequence repeated at least 2 times.
#
# **Examples:**
# - 111 (1 repeated 3 times)
# - 12341234 (1234 repeated 2 times)
# - 123123123 (123 repeated 3 times)
# - 1212121212 (12 repeated 5 times)
# - 1111111 (1 repeated 7 times)
# - 565656 (56 repeated 3 times)
# - 824824824 (824 repeated 3 times)
#
# **Algorithm:**
# 1. Find first digit
# 2. Find next occurrence of first digit to determine potential pattern length
# 3. Extract that pattern
# 4. Check if pattern repeated (len(num) / len(pattern)) times equals the number
# 5. If match and repeats >= 2, it's invalid

# %%
# Part 2: Example data
example_input_2 = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


# %%
def is_invalid_id_part2(num):
    """
    Check if a number is an invalid ID (pattern repeated at least twice).

    Args:
        num: Integer to check

    Returns:
        True if the number is a pattern repeated at least twice, False otherwise
    """
    s = str(num)
    length = len(s)

    # Need at least 2 characters to have a repeating pattern
    if length < 2:
        return False

    # Try all possible pattern lengths (from 1 to len/2)
    # A pattern repeated at least twice means pattern_len <= len/2
    for pattern_len in range(1, length // 2 + 1):
        # Check if this pattern length divides evenly into total length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = length // pattern_len

            # Check if pattern repeated equals the original number
            if pattern * repetitions == s:
                return True

    return False


# %%
# Part 2: Solution function
def solve_part2(data):
    """
    Find and sum all invalid product IDs (patterns repeated at least twice).

    Args:
        data: Input data as string with comma-separated ranges (e.g., "11-22,95-115")

    Returns:
        Sum of all invalid product IDs
    """
    # Parse ranges
    ranges_str = data.strip().split(",")

    total = 0

    for range_str in ranges_str:
        # Parse start and end of range
        start, end = map(int, range_str.split("-"))

        # Check each number in the range
        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                total += num

    return total


# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
# Expected: 4174379265

# %%
# Part 2: Solve with real input
if puzzle_input:
    result_part2 = solve_part2(puzzle_input)
    print(f"Part 2 Answer: {result_part2}")
