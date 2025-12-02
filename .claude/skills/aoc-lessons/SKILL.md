---
name: aoc-lessons
description: Lessons learned from Advent of Code 2025 - common patterns, gotchas, and techniques
---

# Advent of Code 2025 - Lessons Learned

This skill captures patterns, techniques, and lessons learned while solving Advent of Code 2025 puzzles.

## Mandatory Workflows for Each Day

### Before Starting Implementation

1. **Read the problem carefully** - Understand input format, examples, and expected output
2. **Create test file FIRST** - `tests/test_dayXX.py` with example data and expected result
3. **Discuss algorithm approach** - If proposing an algorithm, generate counter-examples to validate robustness
4. **Use superpowers:test-driven-development skill** - Write failing test, then implement

### Implementation Structure

- Solution file: `solutions/dayXX.py`
- Test file: `tests/test_dayXX.py`
- Follow existing patterns from Day 1/Day 2
- Include markdown documentation in solution file
- Separate functions for `solve_part1()` and `solve_part2()`

### Before Committing

1. **Run all tests** - `pytest -v`
2. **Verify both example and real input pass**
3. **Clean up unused variables and imports**
4. **Commit with clear message** - "Add Day X solution: [Problem Name] (both parts complete)"

## Common Patterns

### Pattern: Modulo Arithmetic for Circular/Wrapping Ranges

**When to use:** Problems involving circular structures (dials, rings, cyclic arrays) where values wrap around  
**Example from:** Day 1 (Secret Entrance - dial wrapping from 0-99)  
**Code snippet:**
```python
# For a dial 0-99, moving left/right with wrapping
position = (position - distance) % 100  # Left
position = (position + distance) % 100  # Right
```

### Pattern: String Pattern Matching via Divisor Testing

**When to use:** Detecting if a string/number is composed of a repeating pattern  
**Example from:** Day 2 (Gift Shop - detecting repeated digit sequences)  
**Key insight:** If a pattern repeats N times, the pattern length must divide evenly into the total length  
**Code snippet:**
```python
def has_repeating_pattern(s):
    """Check if string s is a pattern repeated at least twice."""
    length = len(s)
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            if pattern * (length // pattern_len) == s:
                return True
    return False
```

## Gotchas & Pitfalls

### Gotcha: Assuming Even Length for Pattern Matching

**Problem:** Initially assumed repeating patterns would always have even length (pattern repeated exactly twice), missing patterns repeated 3+ times  
**Solution:** Test all divisor lengths, not just len/2. A pattern can repeat any number of times (2, 3, 5, etc.)  
**Examples that break "even length only" assumption:**
- `111` (length 3, pattern "1" × 3)
- `565656` (length 6, pattern "56" × 3)
- `2121212121` (length 10, pattern "21" × 5)
**Learned from:** Day 2 Part 2

### Gotcha: "Find Next Occurrence" Doesn't Cover All Cases

**Problem:** Proposed algorithm: find first digit, find its next occurrence, test that as pattern length. Could miss valid patterns or misidentify boundaries.  
**Why it's risky:** 
- What if first digit appears multiple times but isn't the pattern boundary?
- Example: `52545254` - first digit is `5`, next occurrence at position 2, gives pattern `52`, but multiplying gives `52525252` ≠ `52545254` (correctly invalid, but algorithm is brittle)
**Solution:** Systematically test all divisor lengths rather than relying on character position heuristics  
**Learned from:** Day 2 algorithm discussion

## Useful Utilities

_This section will contain reusable utility functions discovered during puzzle solving._

### Utility: Template Utility Name

**Purpose:** What this utility does  
**Code:**
```python
def utility_function():
    """Description of what this does."""
    pass
```

**Used in:** Day X

## Data Structures & Algorithms

_This section will document algorithmic techniques that proved useful._

### Technique: Template Technique Name

**Use case:** When this technique is applicable  
**Implementation notes:** Key details to remember  
**Seen in:** Day X  
**Reference:**
```python
# Example implementation or key insight
```

## Testing Insights

### Insight: Always Write Tests First (TDD for AoC)

**Observation:** AoC problems come with example inputs and expected outputs - perfect for TDD  
**Application:** 
1. Create test file first with example data
2. Write test that expects the given output
3. Watch it fail
4. Implement solution
5. Test passes = confidence in correctness
**Benefits:**
- Catches off-by-one errors early
- Validates understanding of problem before solving
- Easy regression testing when refactoring
**From:** Day 1 & Day 2 post-mortem

### Insight: Test Both Example and Real Input in Test Suite

**Observation:** Having both example and real input tests catches different types of errors  
**Application:** Structure tests like:
```python
class TestDayXX:
    def test_part1_example(self):
        # Use provided example, assert expected result
        
    def test_part1_solution(self):
        # Use real input, assert actual answer (once known)
```
**Benefits:**
- Example tests verify algorithm correctness
- Real input tests prevent regression after submission
- Both together give confidence in solution robustness
**From:** Day 1 & Day 2 test structure

### Insight: Algorithm Analysis - Always Consider Counter-Examples

**Observation:** When proposing an algorithm, actively search for counter-examples that break it  
**Application:** Before implementing:
1. Propose algorithm
2. Generate 3-5 test cases, including edge cases
3. Mentally trace through algorithm with each case
4. Look for cases where algorithm fails or is ambiguous
5. Refine or choose more robust algorithm
**Example:** Day 2 "find next occurrence" vs "test all divisors" - testing edge cases revealed brittleness  
**From:** Day 2 algorithm discussion

### Insight: Part 2 Often Generalizes Part 1

**Observation:** Part 2 frequently asks for "at least N" instead of "exactly N" or adds complexity  
**Application:** 
- When solving Part 1, consider: "How would this change if the rule was 'at least' instead of 'exactly'?"
- Write helper functions that accept parameters (e.g., `min_repetitions=2`) rather than hardcoding
- Makes refactoring for Part 2 easier
**Examples:**
- Day 1: "ends on 0" → "passes through 0"
- Day 2: "repeated exactly twice" → "repeated at least twice"
**From:** Day 1 & Day 2 pattern

---

## Usage Notes

Update this skill after solving each day's puzzle. Focus on:
- Patterns that could be reused
- Mistakes that could be avoided
- Utilities that could be extracted
- Algorithmic techniques worth remembering
- Testing strategies that worked well
