# %% [markdown]
# # Advent of Code 2025 - Day 3: Lobby Battery Banks
#
# **Problem Summary:**
# Each line represents a bank of batteries with joltage ratings (digits 1-9).
# We need to select batteries to form the largest possible number.
#
# **Part 1:** Select exactly 2 batteries per bank to form the largest 2-digit number.
# Sum the joltages from all banks.
#
# **Part 2:** Select exactly 12 batteries per bank to form the largest 12-digit number.
# Sum the joltages from all banks.
#
# **Key insight:** Greedy selection from left to right - always pick the largest
# digit available while ensuring enough digits remain for future picks.

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day03.txt"):
    with open("../resources/inputs/day03.txt", "r") as f:
        puzzle_input = f.read().strip()
elif os.path.exists("resources/inputs/day03.txt"):
    with open("resources/inputs/day03.txt", "r") as f:
        puzzle_input = f.read().strip()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Part 1: Pick 2 Batteries Per Bank
#
# **Algorithm:**
# For each bank (line):
# 1. Pick 1st digit: Find max digit in positions [0, len-2] (leave room for 1 more)
# 2. Pick 2nd digit: Find max digit after the 1st pick's position
# 3. Form 2-digit number from these picks
# 4. Sum all bank outputs
#
# **Example:**
# - Bank "987654321111111": Pick 9 at pos 0, then 8 at pos 1 → 98
# - Bank "811111111111119": Pick 8 at pos 0, then 9 at pos 14 → 89

# %%
# Part 1: Example data
example_input_1 = """987654321111111
811111111111119
234234234234278
818181911112111"""


# %%
# Part 1: Solution function
def find_max_joltage(bank, num_picks):
    """
    Find the maximum joltage by picking num_picks batteries from a bank.

    Args:
        bank: String of digits representing battery joltages
        num_picks: Number of batteries to select

    Returns:
        Integer formed by the selected digits
    """
    digits = [int(d) for d in bank]
    picked = []
    current_pos = 0

    for pick_num in range(num_picks):
        # How many picks remain after this one
        remaining_picks = num_picks - pick_num - 1

        # Can search from current_pos up to position that leaves room for remaining picks
        search_end = len(digits) - remaining_picks

        # Find the maximum digit in the valid range
        max_digit = max(digits[current_pos:search_end])
        # Find its position (first occurrence)
        max_pos = digits.index(max_digit, current_pos, search_end)

        picked.append(max_digit)
        # Move past this position for next pick
        current_pos = max_pos + 1

    # Form the number from picked digits
    result = int("".join(map(str, picked)))
    return result


def solve_part1(data):
    """
    Find the total output joltage by picking 2 batteries per bank.

    Args:
        data: Input data as string (one bank per line)

    Returns:
        Sum of maximum joltages from all banks
    """
    banks = data.strip().split("\n")
    total = 0

    for bank in banks:
        joltage = find_max_joltage(bank, num_picks=2)
        total += joltage

    return total


# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
print(f"Expected: 357 (98 + 89 + 78 + 92)")

# Let's verify each bank
print("\nBank breakdown:")
for bank in example_input_1.strip().split("\n"):
    joltage = find_max_joltage(bank, 2)
    print(f"  {bank} → {joltage}")

# %%
# Part 1: Solve with real input
if puzzle_input:
    result_part1 = solve_part1(puzzle_input)
    print(f"\nPart 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: Pick 12 Batteries Per Bank
#
# **Algorithm:**
# Same greedy approach, but pick 12 digits instead of 2.
#
# **Example:**
# - Bank "987654321111111": Pick all except some 1s → 987654321111

# %%
# Part 2: Example data
example_input_2 = """987654321111111
811111111111119
234234234234278
818181911112111"""


# %%
# Part 2: Solution function
def solve_part2(data):
    """
    Find the total output joltage by picking 12 batteries per bank.

    Args:
        data: Input data as string (one bank per line)

    Returns:
        Sum of maximum joltages from all banks
    """
    banks = data.strip().split("\n")
    total = 0

    for bank in banks:
        joltage = find_max_joltage(bank, num_picks=12)
        total += joltage

    return total


# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
print(f"Expected: 3121910778619")

# Let's verify each bank
print("\nBank breakdown:")
for bank in example_input_2.strip().split("\n"):
    joltage = find_max_joltage(bank, 12)
    print(f"  {bank} → {joltage}")

# %%
# Part 2: Solve with real input
if puzzle_input:
    result_part2 = solve_part2(puzzle_input)
    print(f"\nPart 2 Answer: {result_part2}")
