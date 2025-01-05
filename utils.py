import numpy as np
from typing import List, Tuple, Optional
from structs import GlobalData, Grid


def find_first_zero_position(matrix: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the first (row, column) index of zero in the matrix.

    Args:
        matrix (np.ndarray): The matrix to search.

    Returns:
        Optional[Tuple[int, int]]: The index of the first zero, or None if not found.
    """
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0:
                return i, j
    return None


def detect_edges(grid: Grid, ids: List[int]) -> List[Tuple[Tuple[int, int], str]]:
    """
    Detects the edges of an element based on boundary conditions (BC) of its nodes.

    Args:
        grid (Grid): The grid containing nodes with coordinates and BC information.
        ids (List[int]): List of nodes IDs defining the element.

    Returns:
        List[Tuple[Tuple[int, int], str]]: A list of detected edges with their labels.
    """
    edges = []
    nodes_position = np.zeros((2, 2), int)

    nodes = [(grid.nodes[node_id - 1], node_id) for node_id in ids]

    min_x = min(node[0].x for node in nodes)
    max_x = max(node[0].x for node in nodes)
    min_y = min(node[0].y for node in nodes)
    max_y = max(node[0].y for node in nodes)

    for node, node_id in nodes:
        if node.x == min_x:
            if node.y == min_y:
                nodes_position[1][0] = node_id
            elif node.y == max_y:
                nodes_position[0][0] = node_id
        elif node.x == max_x:
            if node.y == min_y:
                nodes_position[1][1] = node_id
            elif node.y == max_y:
                nodes_position[0][1] = node_id

    for node_id in ids:
        if node_id not in nodes_position:
            position = find_first_zero_position(nodes_position)
            if position:
                nodes_position[position[0]][position[1]] = node_id

    if grid.nodes[nodes_position[0][0] - 1].BC and grid.nodes[nodes_position[0][1] - 1].BC:
        edges.append(((nodes_position[0][0], nodes_position[0][1]), "top"))
    if grid.nodes[nodes_position[0][1] - 1].BC and grid.nodes[nodes_position[1][1] - 1].BC:
        edges.append(((nodes_position[0][1], nodes_position[1][1]), "right"))
    if grid.nodes[nodes_position[1][1] - 1].BC and grid.nodes[nodes_position[1][0] - 1].BC:
        edges.append(((nodes_position[1][1], nodes_position[1][0]), "bottom"))
    if grid.nodes[nodes_position[1][0] - 1].BC and grid.nodes[nodes_position[0][0] - 1].BC:
        edges.append(((nodes_position[1][0], nodes_position[0][0]), "left"))

    return edges


def get_vector_of_shape_functions(xi: float, eta: float) -> np.ndarray:
    """
    Computes the vector of shape functions.

    Args:
        xi (float): The xi coordinate in the local coordinate system.
        eta (float): The eta coordinate in the local coordinate system.

    Returns:
        np.ndarray: A 4x1 array representing the shape functions at (xi, eta).
    """
    N1 = 0.25 * (1 + xi) * (1 + eta)
    N2 = 0.25 * (1 - xi) * (1 + eta)
    N3 = 0.25 * (1 - xi) * (1 - eta)
    N4 = 0.25 * (1 + xi) * (1 - eta)

    return np.array([[N1], [N2], [N3], [N4]])


def simulate_temp(data: GlobalData, grid: Grid) -> None:
    """
    Simulates temperature changes over time for the grid.

    Args:
        data (GlobalData): Global simulation parameters.
        grid (Grid): Contains the global matrices (C, H) and vector (P) for the simulation.
    """
    temperature_vector = np.full((data.nN, 1), data.initialTemp)

    for _ in range(data.simulationStepTime,
                   data.simulationTime + data.simulationStepTime,
                   data.simulationStepTime):
        C_div_tau = grid.aggregated_C_matrix / data.simulationStepTime
        temperature_vector_next = np.linalg.inv(grid.aggregated_H_matrix + C_div_tau) @ \
                                  (grid.aggregated_P_vector + C_div_tau @ temperature_vector)
        print(np.min(temperature_vector_next), np.max(temperature_vector_next))
        temperature_vector = temperature_vector_next
