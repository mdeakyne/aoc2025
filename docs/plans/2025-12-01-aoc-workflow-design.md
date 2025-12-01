# Advent of Code 2025 Workflow Design

**Date:** 2025-12-01  
**Purpose:** Clean, step-by-step executable solutions with markdown explanations, published to GitLab daily

## Overview

This project contains solutions for Advent of Code 2025, organized as Python files with `#%%` cell markers for interactive execution in Zed editor. Each day's puzzle (with both Part 1 and Part 2) is solved in a single notebook-style file with accompanying pytest tests.

## Project Structure

```
aoc2025/
├── .gitignore           # Excludes resources/, __pycache__, etc.
├── README.md            # Overview, how to run, progress tracker
├── resources/           # NOT synced to GitLab
│   ├── descriptions/
│   │   ├── day01.md
│   │   └── day02.md
│   └── inputs/
│       ├── day01.txt
│       └── day02.txt
├── solutions/           # Published to GitLab
│   ├── day01.py
│   ├── day02.py
│   └── ...
├── tests/               # Published to GitLab
│   ├── test_day01.py
│   ├── test_day02.py
│   └── ...
├── utils/               # Shared helpers (if patterns emerge)
│   └── __init__.py
└── .claude/
    └── skills/
        └── aoc-lessons/
            └── SKILL.md
```

## Git Setup

**.gitignore contents:**
```
resources/
__pycache__/
*.pyc
.DS_Store
*.ipynb_checkpoints/
```

**README.md structure:**
- Link to Advent of Code 2025
- How to run the solutions
- Progress table (Day | Part 1 | Part 2 | Notes)
- Setup instructions

## Solution File Template

Each `dayXX.py` file follows this structure using `#%%` cells:

```python
# %% [markdown]
# # Advent of Code 2025 - Day X: [Puzzle Title]
# 
# **Problem Summary:**
# Brief description of what we're solving
#
# **Approach:**
# High-level strategy for both parts

# %%
# Load input data
with open('../resources/inputs/day01.txt', 'r') as f:
    puzzle_input = f.read().strip()

# %% [markdown]
# ## Part 1: [Part 1 Title]
# 
# Explanation of Part 1 requirements and approach

# %%
# Part 1: Example data
example_input_1 = """example data here"""

# %%
# Part 1: Solution function
def solve_part1(data):
    # Implementation
    pass

# %%
# Part 1: Test with example
result_example_1 = solve_part1(example_input_1)
print(f"Part 1 Example Result: {result_example_1}")
# Expected: [expected value]

# %%
# Part 1: Solve with real input
result_part1 = solve_part1(puzzle_input)
print(f"Part 1 Answer: {result_part1}")

# %% [markdown]
# ## Part 2: [Part 2 Title]
#
# Explanation of Part 2 changes and approach

# %%
# Part 2: Example (may differ from Part 1)
example_input_2 = """example data here"""

# %%
# Part 2: Solution function
def solve_part2(data):
    # Implementation
    pass

# %%
# Part 2: Test with example
result_example_2 = solve_part2(example_input_2)
print(f"Part 2 Example Result: {result_example_2}")
# Expected: [expected value]

# %%
# Part 2: Solve with real input
result_part2 = solve_part2(puzzle_input)
print(f"Part 2 Answer: {result_part2}")
```

**Key principles:**
- Markdown cells explain strategy before code
- Test with examples before real input
- Clear separation between Part 1 and Part 2
- Self-documenting with expected results in comments
- Functions are reusable and testable

## Testing Strategy

Each solution has a corresponding test file (`tests/test_dayXX.py`):

```python
import pytest
from solutions.day01 import solve_part1, solve_part2

# Example data from problem description
EXAMPLE_INPUT_1 = """example data here"""
EXPECTED_PART1 = "expected result"

EXAMPLE_INPUT_2 = """example data here"""
EXPECTED_PART2 = "expected result"


class TestDay01:
    def test_part1_example(self):
        result = solve_part1(EXAMPLE_INPUT_1)
        assert result == EXPECTED_PART1
    
    def test_part2_example(self):
        result = solve_part2(EXAMPLE_INPUT_2)
        assert result == EXPECTED_PART2
    
    # Optional: Test with real input if you want to catch regressions
    def test_part1_solution(self):
        with open('resources/inputs/day01.txt', 'r') as f:
            puzzle_input = f.read().strip()
        result = solve_part1(puzzle_input)
        assert result == YOUR_KNOWN_ANSWER  # Fill in after solving
    
    def test_part2_solution(self):
        with open('resources/inputs/day01.txt', 'r') as f:
            puzzle_input = f.read().strip()
        result = solve_part2(puzzle_input)
        assert result == YOUR_KNOWN_ANSWER  # Fill in after solving
```

## Skills Development

The `.claude/skills/aoc-lessons/SKILL.md` captures lessons learned as puzzles are solved:

```markdown
---
name: aoc-lessons
description: Lessons learned from Advent of Code 2025 - common patterns, gotchas, and techniques
---

# Advent of Code Lessons Learned

## Common Patterns

### Pattern: [Name]
**When to use:** [Description]
**Example from:** Day X
**Code snippet:**
```python
# Example implementation
```

## Gotchas & Pitfalls

### Gotcha: [Name]
**Problem:** What went wrong
**Solution:** How to avoid it
**Learned from:** Day X

## Useful Utilities

### Utility: [Name]
**Purpose:** [Description]
**Code:**
```python
# Reusable utility function
```

## Data Structures & Algorithms

### Technique: [Name]
**Use case:** When this is applicable
**Implementation notes:** Key details
**Seen in:** Day X
```

**Workflow for updating skills:**
- After solving each day, reflect on what was useful, mistakes made, and reusable patterns
- Add entries to SKILL.md incrementally
- Over time, this becomes a personal AoC playbook

## Daily Workflow

**Steps for solving each puzzle:**

1. **Fetch puzzle data** (manual)
   - Save description to `resources/descriptions/dayXX.md`
   - Save input to `resources/inputs/dayXX.txt`

2. **Create solution file**
   - Copy template to `solutions/dayXX.py`
   - Work through problem interactively with `#%%` cells in Zed
   - Run cells with `ctrl-shift-enter`

3. **Extract testable functions**
   - Ensure `solve_part1()` and `solve_part2()` are standalone functions
   - Create `tests/test_dayXX.py` from template

4. **Validate**
   - Run `pytest tests/test_dayXX.py`
   - Ensure examples pass before submitting answers

5. **Update progress**
   - Update README.md progress table
   - Add any lessons to `.claude/skills/aoc-lessons/SKILL.md`

6. **Commit & push to GitLab**
   ```bash
   git add solutions/dayXX.py tests/test_dayXX.py README.md
   git commit -m "Solve Day XX: [Puzzle Title]"
   git push origin main
   ```

**Git commit message conventions:**
- `"Solve Day XX: [Puzzle Title]"` - for completed solutions
- `"Update AoC lessons: [topic]"` - for skill updates
- `"Add Day XX boilerplate"` - if committing before solving

## Dependencies

- Python 3.x
- pytest (for testing)
- Any puzzle-specific libraries as needed

## Success Criteria

- ✅ Clean, readable solutions with markdown explanations
- ✅ Both parts solved in one notebook per day
- ✅ Examples tested before real input
- ✅ All tests passing before GitLab push
- ✅ Lessons captured in local skills
- ✅ Resources folder excluded from version control
