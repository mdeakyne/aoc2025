import pytest

from solutions.day01 import solve_part1, solve_part2

# Example data from problem description
EXAMPLE_INPUT = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

EXPECTED_PART1 = 3  # The dial lands on 0 three times
EXPECTED_PART2 = 6  # The dial points at 0 six times total (including during rotations)


class TestDay01:
    """Tests for Day 1: Secret Entrance."""

    def test_part1_example(self):
        """Test Part 1 with example input.

        Expected path: 50 → 82 → 52 → 0 → 95 → 55 → 0 → 99 → 0 → 14 → 32
        Lands on 0 three times (positions 3, 5, and 7).
        """
        result = solve_part1(EXAMPLE_INPUT)
        assert result == EXPECTED_PART1, f"Expected {EXPECTED_PART1}, got {result}"

    def test_part2_example(self):
        """Test Part 2 with example input.

        Expected: Count every time dial points at 0, including during rotations.
        - L68 from 50→82: passes through 0 once
        - R48 from 52→0: ends at 0 (counted)
        - R60 from 95→55: passes through 0 once
        - L55 from 55→0: ends at 0 (counted)
        - L99 from 99→0: ends at 0 (counted)
        - L82 from 14→32: passes through 0 once
        Total: 6 times
        """
        result = solve_part2(EXAMPLE_INPUT)
        assert result == EXPECTED_PART2, f"Expected {EXPECTED_PART2}, got {result}"

    def test_part1_solution(self):
        """Test Part 1 with real input."""
        with open("resources/inputs/day01.txt", "r") as f:
            puzzle_input = f.read().strip()
        result = solve_part1(puzzle_input)
        assert result == 1055

    def test_part2_solution(self):
        """Test Part 2 with real input."""
        with open("resources/inputs/day01.txt", "r") as f:
            puzzle_input = f.read().strip()
        result = solve_part2(puzzle_input)
        assert result == 6386
