import numpy as np
import math
from typing import List, Tuple, Dict, Literal
from structs import GlobalData, Grid, Element, ElemUniv, JacobiMatrix
from utils import detect_edges, get_vector_of_shape_functions


def calculate_H_matrices(grid: Grid, elem_univ: ElemUniv, conductivity: int) -> None:
    """
    Calculates H matrices for each element

    Args:
        grid (Grid): The grid containing nodes and elements.
        elem_univ (ElemUniv): Universal element data, including shape functions derivatives.
        conductivity (int): Thermal conductivity.
    """

    for element in grid.elements:
        element_nodes_cords = [grid.nodes[element_node - 1] for element_node in element.id]
        x_coords = [node.x for node in element_nodes_cords]
        y_coords = [node.y for node in element_nodes_cords]

        compute_jacobi_matrices(element, elem_univ, x_coords, y_coords)

        for j, jacobi_matrix in enumerate(element.jacobi_matrices):
            H_matrix = compute_H_matrix(j, elem_univ, jacobi_matrix, conductivity)
            element.H_matrices.append(H_matrix)


def compute_jacobi_matrices(element: Element, elem_univ: ElemUniv, x_coords: List[float],
                            y_coords: List[float]) -> None:
    """
    Computes Jacobi matrices for an element and stores them in the element object.

    Args:
        element (Element): The element for which to calculate Jacobi matrices.
        elem_univ (ElemUniv): Universal element data.
        x_coords (List[float]): X coordinates of the element's nodes.
        y_coords (List[float]): Y coordinates of the element's nodes.
    """
    for i in range(len(elem_univ.dN_dxi)):
        jacobi_matrix = JacobiMatrix(elem_univ.dN_dxi[i], elem_univ.dN_deta[i], x_coords, y_coords)
        element.jacobi_matrices.append(jacobi_matrix)


def compute_H_matrix(integration_point_index: int, elem_univ: ElemUniv, jacobi_matrix: JacobiMatrix,
                     conductivity: int) -> np.ndarray:
    """
    Computes the H matrix for a single integration point.

    Args:
        integration_point_index (int): Index of the current integration point.
        elem_univ (ElemUniv): Universal element data.
        jacobi_matrix (JacobiMatrix): Jacobi matrix for the current integration point.
        conductivity (int): Thermal conductivity.

    Returns:
        np.ndarray: The computed H matrix for the integration point.
    """
    inv_matrix = (1 / jacobi_matrix.detJ) * np.array(jacobi_matrix.J1)

    dN_dx, dN_dy = [], []

    for k in range(4):
        dN_dx_dN_dy_mat = np.matmul(inv_matrix,
                                    [[elem_univ.dN_dxi[integration_point_index][k]],
                                     [elem_univ.dN_deta[integration_point_index][k]]])

        dN_dx.append(dN_dx_dN_dy_mat[0][0])
        dN_dy.append(dN_dx_dN_dy_mat[1][0])

    dx_matrix_product = np.outer(dN_dx, dN_dx)
    dy_matrix_product = np.outer(dN_dy, dN_dy)

    return conductivity * (np.array(dx_matrix_product) + np.array(dy_matrix_product)) * jacobi_matrix.detJ


def calculate_Hbc_matrices(data: GlobalData, grid: Grid, weights: List[float],
                           integration_points: Dict[str, List[Tuple[float, int]]]) -> None:
    """
    Calculates Hbc matrices for each element in the grid based on boundary conditions.

    Args:
        data (GlobalData): Contains global simulation properties (alpha).
        grid (Grid): The grid containing nodes and elements.
        weights (List[float]): Weights for integration points.
        integration_points (Dict[str, List[Tuple[float, int]]]): Integration points for each edge type.
    """
    for element in grid.elements:
        Hbc_matrix = np.zeros((4, 4))
        edges = detect_edges(grid, element.id)

        if not edges:
            continue

        for edge_nodes, edge_name in edges:
            node_1 = grid.nodes[edge_nodes[0] - 1]
            node_2 = grid.nodes[edge_nodes[1] - 1]

            edge_length = math.sqrt(math.pow(node_2.x - node_1.x, 2) + math.pow(node_2.y - node_1.y, 2))
            ds = edge_length / 2

            edge_matrix = np.zeros((4, 4))
            for index, (xi, eta) in enumerate(integration_points[edge_name]):
                shape_vector = get_vector_of_shape_functions(xi, eta)
                edge_matrix += weights[index] * np.outer(shape_vector, shape_vector.T)

            Hbc_matrix += data.alfa * edge_matrix * ds

        element.Hbc_matrix += Hbc_matrix


def calculate_C_matrices(data: GlobalData, grid: Grid, integration_points: List[Tuple[float, float]]) -> None:
    for element in grid.elements:
        for index, (xi, eta) in enumerate(integration_points):
            N_vector = [[0.25 * (1 - xi) * (1 - eta)],
                        [0.25 * (1 + xi) * (1 - eta)],
                        [0.25 * (1 + xi) * (1 + eta)],
                        [0.25 * (1 - xi) * (1 + eta)]]
            C_matrix = data.density * data.specificHeat * (np.array(N_vector) * np.array(N_vector).T) * \
                       element.jacobi_matrices[index].detJ
            element.C_matrices.append(C_matrix)


def integrate_matrices(elements: List[Element], matrix_type: Literal['H', 'C'], weights: List[List[float]],
                       integration_points: List[Tuple[float, float]]) -> None:
    """
    Integrates matrices of a given type for all elements in the grid.

    Args:
        elements (List[Element]): List of elements in the grid.
        matrix_type (Literal['H', 'C']): Type of the matrix to be integrated.
        weights (List[List[float]]): Gaussian quadrature for integration points.
        integration_points (List[Tuple[float, float]]): List of integration points in 2D surface.
    """
    num_points = int(math.sqrt(len(integration_points)))

    for element in elements:
        matrix = np.zeros((4, 4))
        for k, (i, j) in enumerate([(i, j) for i in range(num_points) for j in range(num_points)]):
            matrix += element[matrix_type + '_matrices'][k] * weights[i][j] * weights[j][i]
        element['integrated_' + matrix_type + '_matrix'] = matrix


def aggregate_matrices(grid: Grid, matrix_type: Literal['H', 'C']) -> None:
    """
    Aggregates all matrices of a given type from each element in one matrix for the entire grid.

    Args:
        grid (Grid): The grid containing nodes, elements and the global integrated matrix.
        matrix_type (Literal['H', 'C']): Type of the matrix to be aggregated.
    """

    for element in grid.elements:
        element_matrix = element['integrated_' + matrix_type + '_matrix']
        for i in range(4):
            for j in range(4):
                global_row = element.id[i]
                global_column = element.id[j]
                grid['aggregated_' + matrix_type + '_matrix'][global_row - 1][global_column - 1] += element_matrix[i][j]
