import math
import numpy as np
from typing import List, Tuple, Dict
from structs import GlobalData, Grid
from utils import detect_edges, get_vector_of_shape_functions


def calculate_P_vector(data: GlobalData, grid: Grid, weights: List[float],
                       integration_points: Dict[str, List[Tuple[float, int]]]) -> None:
    """
    Calculates the P vector for each element based on boundary conditions.

    Args:
        data (GlobalData): Global simulation properties (alpha, temperature, etc.).
        grid (Grid): The grid containing elements and nodes.
        weights (List[float]): Weights for integration points.
        integration_points (Dict[str, List[Tuple[float, int]]]): Integration points for each edge.
    """
    for element in grid.elements:
        P_vector = np.zeros((4, 1))
        edges = detect_edges(grid, element.id)

        if not edges:
            continue

        for edge_nodes, edge_name in edges:
            node_1 = grid.nodes[edge_nodes[0] - 1]
            node_2 = grid.nodes[edge_nodes[1] - 1]

            edge_length = math.sqrt(math.pow(node_2.x - node_1.x, 2) + math.pow(node_2.y - node_1.y, 2))
            ds = edge_length / 2

            edge_vector_sum = np.zeros((4, 1))
            for index, (xi, eta) in enumerate(integration_points[edge_name]):
                shape_vector = get_vector_of_shape_functions(xi, eta)
                edge_vector_sum += data.alfa * data.tot * weights[index] * shape_vector

            P_vector += edge_vector_sum * ds

        element.P_vector = P_vector


def aggregate_P_vectors(grid: Grid) -> None:
    """
    Aggregates P vectors from all elements into a single global P vector for the grid.

    Args:
        grid (Grid): The grid containing aggregated P vector.
    """
    for element in grid.elements:
        for local_index, global_node_id in enumerate(element.id):
            grid.aggregated_P_vector[global_node_id - 1][0] += element.P_vector[local_index][0]
