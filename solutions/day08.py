# %% [markdown]
# # Advent of Code 2025 - Day 8: Playground
#
# **Problem Summary:**
# Junction boxes suspended in 3D space need to be connected with light strings.
# Connect the 1000 closest pairs to form circuits (connected components).
# Find the product of the 3 largest circuit sizes.
#
# **Algorithm:**
# 1. Parse 3D coordinates (x, y, z)
# 2. Calculate all pairwise Euclidean distances
# 3. Sort pairs by distance (shortest first)
# 4. Add first 1000 edges to NetworkX graph
# 5. Find connected components (circuits)
# 6. Multiply sizes of 3 largest circuits

# %%
# Load input data
import os
from math import sqrt

import networkx as nx

if os.path.exists("../resources/inputs/day08.txt"):
    with open("../resources/inputs/day08.txt", "r") as f:
        puzzle_input = f.read()
elif os.path.exists("resources/inputs/day08.txt"):
    with open("resources/inputs/day08.txt", "r") as f:
        puzzle_input = f.read()
else:
    puzzle_input = ""  # Will be loaded when needed

# %% [markdown]
# ## Helper Functions


# %%
def parse_coordinates(data):
    """Parse junction box coordinates from input."""
    boxes = []
    for line in data.strip().split("\n"):
        x, y, z = map(int, line.split(","))
        boxes.append((x, y, z))
    return boxes


def euclidean_distance(box1, box2):
    """Calculate 3D Euclidean distance between two boxes."""
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def calculate_all_distances(boxes):
    """Calculate distances for all pairs of boxes."""
    distances = []
    n = len(boxes)

    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(boxes[i], boxes[j])
            distances.append((dist, i, j))

    return distances


def build_graph_with_shortest_edges(boxes, num_connections):
    """
    Build graph by connecting the num_connections shortest pairs.
    Returns NetworkX graph.
    """
    # Calculate all pairwise distances
    distances = calculate_all_distances(boxes)

    # Sort by distance (shortest first)
    distances.sort()

    # Create graph with all nodes
    G = nx.Graph()
    G.add_nodes_from(range(len(boxes)))

    # Add the shortest edges
    for i in range(min(num_connections, len(distances))):
        dist, box1, box2 = distances[i]
        G.add_edge(box1, box2)

    return G


def get_circuit_sizes(G):
    """Get sizes of all connected components (circuits)."""
    components = nx.connected_components(G)
    sizes = [len(component) for component in components]
    return sorted(sizes, reverse=True)


# %% [markdown]
# ## Part 1: Connect 1000 Shortest Pairs


# %%
def solve_part1(data, num_connections=1000):
    """Connect the shortest num_connections pairs and find product of 3 largest circuits."""
    boxes = parse_coordinates(data)

    # Build graph with shortest connections
    G = build_graph_with_shortest_edges(boxes, num_connections)

    # Get circuit sizes
    sizes = get_circuit_sizes(G)

    # Multiply 3 largest
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
    else:
        result = 0

    return result, sizes


# %%
# Part 1: Example (connect 10 shortest pairs)
example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

example_result, example_sizes = solve_part1(example_input, num_connections=10)
print(f"Part 1 Example Result: {example_result}")
print(f"Circuit sizes: {example_sizes}")
print(f"Number of circuits: {len(example_sizes)}")
print(f"Expected: 40 (product of 5 * 4 * 2)")
print(f"Expected: 11 circuits")

# %%
# Part 1: Solution (connect 1000 shortest pairs)
part1_answer, part1_sizes = solve_part1(puzzle_input, num_connections=1000)
print(f"Part 1 Answer: {part1_answer}")
print(f"Number of circuits: {len(part1_sizes)}")
print(f"Three largest circuits: {part1_sizes[:3]}")

# %% [markdown]
# ## Part 2: Connect Until Single Circuit


# %%
def solve_part2(data):
    """
    Continue connecting closest pairs until all boxes are in one circuit.
    Return product of X coordinates of the final connecting edge.
    """
    boxes = parse_coordinates(data)

    # Calculate all pairwise distances
    distances = calculate_all_distances(boxes)

    # Sort by distance (shortest first)
    distances.sort()

    # Create graph with all nodes
    G = nx.Graph()
    G.add_nodes_from(range(len(boxes)))

    # Add edges one by one until we have a single component
    for dist, box1_idx, box2_idx in distances:
        # Check if these boxes are already in the same component
        if nx.has_path(G, box1_idx, box2_idx):
            continue

        # Add edge
        G.add_edge(box1_idx, box2_idx)

        # Check if we now have a single component
        num_components = nx.number_connected_components(G)
        if num_components == 1:
            # This is the final edge!
            x1 = boxes[box1_idx][0]
            x2 = boxes[box2_idx][0]
            return x1 * x2

    return 0


# %%
# Part 2: Example
example_result_p2 = solve_part2(example_input)
print(f"Part 2 Example Result: {example_result_p2}")
print(f"Expected: 25272 (216 * 117)")

# %%
# Part 2: Solution
part2_answer = solve_part2(puzzle_input)
print(f"Part 2 Answer: {part2_answer}")
