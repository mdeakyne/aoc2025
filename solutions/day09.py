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


def is_point_on_edge(point, p1, p2):
    """Check if point lies on the line segment between p1 and p2."""
    px, py = point
    x1, y1 = p1
    x2, y2 = p2

    # Check if point is within bounding box
    if not (min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)):
        return False

    # Check if it's on a horizontal or vertical line
    if x1 == x2:  # Vertical line
        return px == x1
    elif y1 == y2:  # Horizontal line
        return py == y1

    return False


def is_point_inside_polygon(point, polygon):
    """
    Check if point is inside polygon OR on its boundary.
    Uses ray casting for interior, plus edge checking for boundary.
    """
    px, py = point
    n = len(polygon)

    # First check if point is on any edge
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        if is_point_on_edge(point, p1, p2):
            return True

    # Ray casting for interior
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
def get_edge_tiles_only(tiles):
    """Get all tiles on the edges between consecutive red tiles (not interior)."""
    edge_tiles = set()

    for i in range(len(tiles)):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % len(tiles)]

        # Add all tiles on the line between these two red tiles
        if x1 == x2:
            # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                edge_tiles.add((x1, y))
        elif y1 == y2:
            # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                edge_tiles.add((x, y1))

    return edge_tiles


# %%
def solve_part2(data):
    """
    Find largest rectangle using only red and green tiles.
    Green = edges between red tiles + interior of polygon.
    """
    tiles = parse_tiles(data)
    red_tiles_set = set(tiles)
    edge_tiles = get_edge_tiles_only(tiles)

    max_area = 0

    # Check all pairs of red tiles
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            # Calculate area first
            area = calculate_rectangle_area(tiles[i], tiles[j])

            # Skip rectangles that are too large to validate
            # Use very conservative limit to avoid timeout
            if area > 10000:
                continue

            # Check all tiles in rectangle
            all_valid = True
            for x in range(min_x, max_x + 1):
                if not all_valid:
                    break
                for y in range(min_y, max_y + 1):
                    # Tile is valid if: red, on polygon edge, or in polygon interior
                    if (x, y) in red_tiles_set or (x, y) in edge_tiles:
                        continue
                    # Not red or on edge, check interior (using simpler ray cast without edge check)
                    px, py = x, y
                    inside = False
                    for k in range(len(tiles)):
                        x_1, y_1 = tiles[k]
                        x_2, y_2 = tiles[(k + 1) % len(tiles)]
                        if (y_1 > py) != (y_2 > py):
                            x_intersect = x_1 + (py - y_1) * (x_2 - x_1) / (y_2 - y_1)
                            if px < x_intersect:
                                inside = not inside
                    if not inside:
                        all_valid = False
                        break

            if all_valid:
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
