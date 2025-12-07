# %% [markdown]
# # Advent of Code 2025 - Day 6: Trash Compactor
#
# **Problem Summary:**
# Math worksheet with problems arranged vertically in columns.
# - Each column is a separate problem
# - Numbers are stacked vertically
# - Last row contains the operator (`+` or `*`)
# - Numbers separated by whitespace
# - Calculate each problem, sum all results
#
# **Approach:**
# 1. Split rows by whitespace to get tokens
# 2. Match tokens by column index (token 0 from each row = problem 1, etc.)
# 3. Apply operator to each problem's numbers
# 4. Sum all problem results

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day06.txt"):
    with open("../resources/inputs/day06.txt", "r") as f:
        puzzle_input = f.read()
elif os.path.exists("resources/inputs/day06.txt"):
    with open("resources/inputs/day06.txt", "r") as f:
        puzzle_input = f.read()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Part 1: Solve Math Worksheet
#
# **Key insight:** Numbers are space-separated, so we can split each row
# and match by column index!

# %%
# Part 1: Example data
example_input_1 = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """


# %%
# Helper function: Apply operation to list of numbers
def apply_operation(numbers, operator):
    """
    Apply an operation to a list of numbers sequentially.

    Args:
        numbers: List of integers
        operator: '+' or '*'

    Returns:
        Result of applying the operation
    """
    if not numbers:
        return 0

    result = numbers[0]
    for num in numbers[1:]:
        if operator == "+":
            result += num
        elif operator == "*":
            result *= num

    return result


# %%
# Part 1: Solution function
def solve_part1(data):
    """
    Solve the math worksheet and return the grand total.

    Args:
        data: Input data as string (multi-line worksheet)

    Returns:
        Grand total (sum of all problem results)
    """
    lines = [line for line in data.split("\n") if line.strip()]

    # Last line contains operators, other lines contain numbers
    number_rows = lines[:-1]
    operator_row = lines[-1]

    # Split each row by whitespace to get individual tokens
    number_tokens_per_row = [row.split() for row in number_rows]
    operator_tokens = operator_row.split()

    # Each column index corresponds to one problem
    num_problems = len(operator_tokens)
    grand_total = 0

    for prob_idx in range(num_problems):
        # Collect numbers from each row for this problem index
        numbers = []
        for row_tokens in number_tokens_per_row:
            if prob_idx < len(row_tokens):
                numbers.append(int(row_tokens[prob_idx]))

        # Get the operator for this problem
        operator = operator_tokens[prob_idx]

        # Calculate result
        result = apply_operation(numbers, operator)
        grand_total += result

    return grand_total


# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
print(f"Expected: 4277556")

# Show breakdown
lines = [line for line in example_input_1.split("\n") if line.strip()]
number_rows = lines[:-1]
operator_row = lines[-1]
number_tokens_per_row = [row.split() for row in number_rows]
operator_tokens = operator_row.split()

print("\nProblem breakdown:")
for prob_idx in range(len(operator_tokens)):
    numbers = []
    for row_tokens in number_tokens_per_row:
        if prob_idx < len(row_tokens):
            numbers.append(int(row_tokens[prob_idx]))
    operator = operator_tokens[prob_idx]
    result = apply_operation(numbers, operator)
    print(
        f"  Problem {prob_idx + 1}: {' '.join(map(str, numbers))} {operator} = {result}"
    )

# %%
# Part 1: Solve with real input
if puzzle_input:
    result_part1 = solve_part1(puzzle_input)
    print(f"\nPart 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: Cephalopod Math (Right-to-Left, Vertical Numbers)
#
# **New reading rules:**
# - Read columns **right-to-left**
# - Each column represents a number
# - Numbers are written **vertically** (top = most significant digit)
# - Empty columns separate problems
# - Bottom row contains operator

# %%
# Part 2: Example data
example_input_2 = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """


# %%
# Part 2: Solution function
def solve_part2(data):
    """
    Solve the math worksheet reading right-to-left with vertical numbers.

    Args:
        data: Input data as string (multi-line worksheet)

    Returns:
        Grand total (sum of all problem results)
    """
    lines = data.split("\n")

    # Pad all lines to same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Process columns right-to-left
    problems = []
    current_problem = []

    for col_idx in range(max_len - 1, -1, -1):
        # Extract column
        column = "".join(line[col_idx] for line in lines)

        # Check if empty column (separator)
        if column.strip() == "":
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            # Add to current problem (we'll reverse later since we're going right-to-left)
            current_problem.append(column)

    # Don't forget last problem
    if current_problem:
        problems.append(current_problem)

    # Solve each problem
    grand_total = 0

    for problem_cols in problems:
        # Reverse columns since we collected them right-to-left
        problem_cols = problem_cols[::-1]

        # Extract numbers and operator from columns
        numbers = []
        operator = None

        for col in problem_cols:
            # Strip the column first, then check last char
            col_stripped = col.strip()

            if not col_stripped:
                continue

            # Last character should be from operator row
            last_char = col_stripped[-1]

            if last_char in "+*":
                # This column has the operator
                operator = last_char
                # Number is formed from all characters except operator
                number_chars = col_stripped[:-1]
                if number_chars:
                    numbers.append(int(number_chars))
            else:
                # Regular number column - all digits
                numbers.append(int(col_stripped))

        # Calculate result
        if operator and numbers:
            result = apply_operation(numbers, operator)
            grand_total += result

    return grand_total


# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
print(f"Expected: 3263827")

# %%
# Part 2: Solve with real input
if puzzle_input:
    result_part2 = solve_part2(puzzle_input)
    print(f"\nPart 2 Answer: {result_part2}")
