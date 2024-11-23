import math
import sys
import pandas as pd
import numpy as np
from typing import List, Tuple

import structs


def read_file(file_name: str):
    """Reads the input file and parses nodes, elements, and field values"""

    elements, nodes, field_values = [], [], []
    node_lines = element_lines = False

    with open(file_name, 'r') as file:
        for line in file:

            if line.startswith("*Node"):
                node_lines = True
                continue
            elif line.startswith("*Element,"):
                node_lines, element_lines = False, True
                continue
            elif line.startswith("*BC"):
                break

            line_array = [x for x in line.strip().split(" ") if x]

            if element_lines:
                element = structs.Element([int(val.replace(',', '')) for val in line_array[1:5]])
                elements.append(element)
            elif node_lines:
                node = structs.Node(float(line_array[1].replace(',', '')), float(line_array[2]))
                nodes.append(node)

            elif line_array[0] in {"Nodes", "Elements"}:
                field_values.append(int(line_array[2]))
            elif not element_lines and not node_lines:
                field_values.append(int(line_array[1]))

    return elements, nodes, field_values


def calculate_H_matrices(grid: structs.Grid, elem_univ: structs.ElemUniv, conductivity: int,
                         integration_points: List[Tuple[float, float]]):
    """Calculates H matrices for each element"""

    for element in grid.elements:
        element_nodes_cords = [grid.nodes[element_node - 1] for element_node in element.id]
        x_coords = [node.x for node in element_nodes_cords]
        y_coords = [node.y for node in element_nodes_cords]

        for i in range(len(integration_points)):
            matrix = structs.JacobiMatrix(elem_univ.dN_dxi[i], elem_univ.dN_deta[i], x_coords, y_coords)
            element.jacobi_matrices.append(matrix)

    for i, element in enumerate(elements):
        for j in range(len(integration_points)):
            inv_matrix = (1 / element.jacobi_matrices[j].detJ) * np.array(element.jacobi_matrices[j].J1)

            dN_dx, dN_dy = [], []
            for k in range(4):
                dN_dx_dN_dy_mat = np.matmul(inv_matrix, [[elem_univ.dN_dxi[j][k]], [elem_univ.dN_deta[j][k]]])

                dN_dx.append(dN_dx_dN_dy_mat[0][0])
                dN_dy.append(dN_dx_dN_dy_mat[1][0])

            dx_matrix_product = np.outer(dN_dx, dN_dx)
            dy_matrix_product = np.outer(dN_dy, dN_dy)

            element.H_matrices.append(
                conductivity * (np.array(dx_matrix_product) + np.array(dy_matrix_product)) *
                element.jacobi_matrices[j].detJ)


def integrate_H_matrices(elements: List[structs.Element], weights: List[List[float]],
                         integration_points: List[Tuple[float, float]]):
    """Integrates H matrices for all elements"""

    len_1 = int(math.sqrt(len(integration_points)))
    for element in elements:
        H_matrix = np.zeros((4, 4))
        for k, (i, j) in enumerate([(i, j) for i in range(len_1) for j in range(len_1)]):
            H_matrix += element.H_matrices[k] * weights[i][j] * weights[j][i]
        element.integrated_H_matrix = H_matrix


def aggregate_H_matrices(grid: structs.Grid):
    """Aggregates all H matrices from each element in one matrix for the entire grid"""

    for element in grid.elements:
        for _, (i, j) in enumerate((i, j) for i in range(4) for j in range(4)):
            row = element.id[i]
            column = element.id[j]
            grid.aggregated_H_matrix[row - 1][column - 1] += element.integrated_H_matrix[i][j]


file_name = sys.argv[1] if len(sys.argv) > 1 else None

try:
    if not file_name:
        raise FileNotFoundError("Podaj nazwe pliku, z ktorego chcesz odczytac, jako argument")

    elements, nodes, field_values = read_file(file_name)

    data = structs.GlobalData(*field_values[:10])
    grid = structs.Grid(nN=field_values[-2], nE=field_values[-1], elements=elements, nodes=nodes)

    # integration_points = [(-1 / math.sqrt(3), -1 / math.sqrt(3)), (-1 / math.sqrt(3), 1 / math.sqrt(3)),
    #                       (1 / math.sqrt(3), 1 / math.sqrt(3)), (1 / math.sqrt(3), -1 / math.sqrt(3))]

    # weights = [[1, 1], [1, 1]]

    integration_points = [(-math.sqrt(3 / 5), -math.sqrt(3 / 5)), (0, -math.sqrt(3 / 5)),
                          (math.sqrt(3 / 5), -math.sqrt(3 / 5)),
                          (-math.sqrt(3 / 5), 0), (0, 0), (math.sqrt(3 / 5), 0),
                          (-math.sqrt(3 / 5), math.sqrt(3 / 5)), (0, math.sqrt(3 / 5)),
                          (math.sqrt(3 / 5), math.sqrt(3 / 5))]

    weights = [[5 / 9, 8 / 9, 5 / 9],
               [5 / 9, 8 / 9, 5 / 9],
               [5 / 9, 8 / 9, 5 / 9]]

    elem_univ = structs.ElemUniv(integration_points)

    calculate_H_matrices(grid, elem_univ, data.conductivity, integration_points)
    integrate_H_matrices(elements, weights, integration_points)
    aggregate_H_matrices(grid)

except ValueError as e:
    print(f"Value Error: {e}")
except FileNotFoundError as e:
    print(f"File Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
