import numpy as np
from typing import List, Tuple

from structs import GlobalData, Grid


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

    def sort_nodes(nodes, sort_key):
        return sorted(((grid.nodes[node_id - 1], node_id) for node_id in nodes), key=sort_key)

    sorted_nodes_vertically = sort_nodes(ids, lambda item: (item[0].x, item[0].y))
    sorted_nodes_horizontally = sort_nodes(ids, lambda item: (item[0].x, -item[0].y))

    nodes_position[1][0] = sorted_nodes_vertically[0][1]
    nodes_position[0][1] = sorted_nodes_vertically[-1][1]
    nodes_position[0][0] = sorted_nodes_horizontally[0][1]
    nodes_position[1][1] = sorted_nodes_horizontally[-1][1]

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
    temperature_vector = np.full((16, 1), data.initialTemp)

    for _ in range(data.simulationStepTime,
                   data.simulationTime + data.simulationStepTime,
                   data.simulationStepTime):
        C_div_tau = grid.aggregated_C_matrix / data.simulationStepTime
        temperature_vector_next = np.linalg.inv(grid.aggregated_H_matrix + C_div_tau) @ \
                                  (grid.aggregated_P_vector + C_div_tau @ temperature_vector)
        print(np.min(temperature_vector_next), np.max(temperature_vector_next))
        temperature_vector = temperature_vector_next
