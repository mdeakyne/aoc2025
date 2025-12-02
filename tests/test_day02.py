import pytest

from solutions.day02 import solve_part1, solve_part2

# Example data from problem description
EXAMPLE_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

EXPECTED_PART1 = 1227775554  # Sum of invalid IDs (pattern repeated exactly twice)
EXPECTED_PART2 = 4174379265  # Sum of invalid IDs (pattern repeated at least twice)


class TestDay02:
    """Tests for Day 2: Gift Shop."""

    def test_part1_example(self):
        """Test Part 1 with example input.

        Expected invalid IDs (pattern repeated exactly twice):
        - 11-22: 11, 22
        - 95-115: 99
        - 998-1012: 1010
        - 1188511880-1188511890: 1188511885
        - 222220-222224: 222222
        - 446443-446449: 446446
        - 38593856-38593862: 38593859
        Total: 1227775554
        """
        result = solve_part1(EXAMPLE_INPUT)
        assert result == EXPECTED_PART1, f"Expected {EXPECTED_PART1}, got {result}"

    def test_part2_example(self):
        """Test Part 2 with example input.

        Expected invalid IDs (pattern repeated at least twice):
        - All from Part 1, plus:
        - 95-115: 111 (1 repeated 3 times)
        - 998-1012: 999 (9 repeated 3 times)
        - 565653-565659: 565656 (56 repeated 3 times)
        - 824824821-824824827: 824824824 (824 repeated 3 times)
        - 2121212118-2121212124: 2121212121 (21 repeated 5 times)
        Total: 4174379265
        """
        result = solve_part2(EXAMPLE_INPUT)
        assert result == EXPECTED_PART2, f"Expected {EXPECTED_PART2}, got {result}"

    def test_part1_solution(self):
        """Test Part 1 with real input."""
        with open("resources/inputs/day02.txt", "r") as f:
            puzzle_input = f.read().strip()
        result = solve_part1(puzzle_input)
        assert result == 35367539282

    def test_part2_solution(self):
        """Test Part 2 with real input."""
        with open("resources/inputs/day02.txt", "r") as f:
            puzzle_input = f.read().strip()
        result = solve_part2(puzzle_input)
        assert result == 45814076230
