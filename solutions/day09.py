# %% [markdown]
# # Advent of Code 2025 - Day 9: Movie Theater
#
# **Problem Summary:**
# Find the largest rectangle that can be formed using two red tiles as opposite corners.
# Rectangle area = |x2 - x1| × |y2 - y1|
#
# **Approach:**
# 1. Parse red tile coordinates (x, y)
# 2. Calculate area for all pairs of tiles
# 3. Return maximum area

# %%
# Load input data
import os

if os.path.exists("../resources/inputs/day09.txt"):
    with open("../resources/inputs/day09.txt", "r") as f:
        puzzle_input = f.read()
elif os.path.exists("resources/inputs/day09.txt"):
    with open("resources/inputs/day09.txt", "r") as f:
        puzzle_input = f.read()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Helper Functions


# %%
def parse_tiles(data):
    """Parse red tile coordinates from input."""
    tiles = []
    for line in data.strip().split("\n"):
        x, y = map(int, line.split(","))
        tiles.append((x, y))
    return tiles


def calculate_rectangle_area(tile1, tile2):
    """
    Calculate area of rectangle formed by two opposite corners.
    Uses inclusive counting since the tiles themselves are corners.
    """
    x1, y1 = tile1
    x2, y2 = tile2
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


# %% [markdown]
# ## Part 1: Find Largest Rectangle


# %%
def solve_part1(data):
    """Find the largest rectangle using any two red tiles as opposite corners."""
    tiles = parse_tiles(data)

    max_area = 0

    # Check all pairs of tiles
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_rectangle_area(tiles[i], tiles[j])
            max_area = max(max_area, area)

    return max_area


# %%
# Part 1: Example
example_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

example_result = solve_part1(example_input)
print(f"Part 1 Example Result: {example_result}")
print(f"Expected: 50")

# %%
# Part 1: Solution
part1_answer = solve_part1(puzzle_input)
print(f"Part 1 Answer: {part1_answer}")

# %% [markdown]
# ## Part 2: Restrict to Red/Green Tiles Only


# %%
def get_green_tiles(tiles):
    """
    Build the set of green tiles.
    Green tiles include:
    1. All tiles along edges between consecutive red tiles
    2. All tiles inside the polygon formed by red tiles
    """
    green_tiles = set()

    # Add edge tiles between consecutive red tiles
    for i in range(len(tiles)):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % len(tiles)]  # Wrap to first tile

        # Add all tiles on the line between these two red tiles
        if x1 == x2:
            # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                green_tiles.add((x1, y))
        elif y1 == y2:
            # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                green_tiles.add((x, y1))

    # Add interior tiles using point-in-polygon
    # Find bounding box
    min_x = min(x for x, y in tiles)
    max_x = max(x for x, y in tiles)
    min_y = min(y for x, y in tiles)
    max_y = max(y for x, y in tiles)

    # Check each point in bounding box
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if is_point_inside_polygon((x, y), tiles):
                green_tiles.add((x, y))

    return green_tiles


def is_point_inside_polygon(point, polygon):
    """
    Ray casting algorithm to determine if point is inside polygon.
    Cast a ray from point to the right and count intersections with edges.
    Odd count = inside, even count = outside.
    """
    px, py = point
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Check if ray crosses this edge
        if (y1 > py) != (y2 > py):
            # Calculate x coordinate of intersection
            x_intersect = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < x_intersect:
                inside = not inside

    return inside


def is_rectangle_valid(tile1, tile2, red_tiles_set, green_tiles):
    """
    Check if all tiles in the rectangle are red or green.
    """
    x1, y1 = tile1
    x2, y2 = tile2

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # Check all tiles in rectangle
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in red_tiles_set and (x, y) not in green_tiles:
                return False

    return True


# %%
def solve_part2(data):
    """
    Find largest rectangle using only red and green tiles.

    Key insight: We don't need to check every tile in the rectangle.
    The polygon is axis-aligned (edges are horizontal or vertical).
    A rectangle is valid if all four corners are inside or on the polygon boundary.
    """
    tiles = parse_tiles(data)
    red_tiles_set = set(tiles)

    max_area = 0

    # Check all pairs of red tiles
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            # The four corners of the rectangle
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]

            # Check if all corners are inside or on the polygon
            # For axis-aligned polygons, if all corners are in, the whole rectangle is in
            all_valid = True
            for corner in corners:
                # Corner is valid if it's red or inside the polygon
                if corner not in red_tiles_set and not is_point_inside_polygon(
                    corner, tiles
                ):
                    all_valid = False
                    break

            if all_valid:
                area = calculate_rectangle_area(tiles[i], tiles[j])
                max_area = max(max_area, area)

    return max_area


# %%
# Part 2: Example
example_result_p2 = solve_part2(example_input)
print(f"Part 2 Example Result: {example_result_p2}")
print(f"Expected: 24")

# %%
# Part 2: Solution
part2_answer = solve_part2(puzzle_input)
print(f"Part 2 Answer: {part2_answer}")
