import math
import sys
import pandas as pd
import numpy as np

import structs

data = None
grid = None


def read_file(file_name):
    elements, nodes, field_values = [], [], []
    node_lines = element_lines = False

    with open(file_name, 'r') as file:
        field_values = []
        for line in file:
            line_array = [x for x in line.strip().split(" ") if x]

            if str(line_array[0]) == '*Node':
                node_lines = True
                continue
            elif str(line_array[0]) == '*Element,':
                node_lines, element_lines = False, True
                continue
            elif str(line_array[0]) == '*BC':
                break

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


file_name = sys.argv[1] if len(sys.argv) > 1 else None

try:
    if not file_name:
        raise Exception("Podaj nazwe pliku, z ktorego chcesz odczytac, jako argument")

    elements, nodes, field_values = read_file(file_name)

    data = structs.GlobalData(*field_values[:10])
    grid = structs.Grid(nN=field_values[-2], nE=field_values[-1], elements=elements, nodes=nodes)

    # for field in data.__dataclass_fields__:
    #     value = getattr(data, field)
    #     print(f"""{field}: {value}""")
    #
    # print("\n")
    #
    # for index, node in enumerate(nodes):
    #     print(f"""node {index}: {node.x}\t{node.y}""")
    # #
    # print("\n")
    # #
    # for index, element in enumerate(elements):
    #     print(f"""element {index}: {element.id}""")

    # integration_points = [(-1 / math.sqrt(3), -1 / math.sqrt(3)), (-1 / math.sqrt(3), 1 / math.sqrt(3)),
    #                       (1 / math.sqrt(3), 1 / math.sqrt(3)), (1 / math.sqrt(3), -1 / math.sqrt(3))]

    # weights = [[1, 1], [1, 1]]

    integration_points = [(-math.sqrt(3/5), -math.sqrt(3/5)), (0, -math.sqrt(3/5)), (math.sqrt(3/5), -math.sqrt(3/5)),
                          (-math.sqrt(3/5), 0), (0, 0), (math.sqrt(3/5), 0),
                          (-math.sqrt(3/5), math.sqrt(3/5)), (0, math.sqrt(3/5)), (math.sqrt(3/5), math.sqrt(3/5))]

    weights = [[5/9, 8/9, 5/9], [5/9, 8/9, 5/9], [5/9, 8/9, 5/9]]

    elem_univ = structs.ElemUniv(integration_points)

    for element in elements:
        element_nodes_cords = [nodes[element_node - 1] for element_node in element.id]
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

            dx_matrix_product = []
            dy_matrix_product = []

            for k in range(4):
                dx_matrix_product.append([dN_dx[k] * dN_dx[m] for m in range(4)])
            for k in range(4):
                dy_matrix_product.append([dN_dy[k] * dN_dy[m] for m in range(4)])

            element.H_matrices.append(
                data.conductivity * (np.array(dx_matrix_product) + np.array(dy_matrix_product)) *
                element.jacobi_matrices[j].detJ)

    len_1 = int(math.sqrt(len(integration_points)))
    for element in elements:
        H_matrix = np.zeros((4, 4))
        for k, (i, j) in enumerate([(i, j) for i in range(len_1) for j in range(len_1)]):
            H_matrix += element.H_matrices[k] * weights[i][j] * weights[j][i]
        element.integrated_H_matrix = H_matrix

except Exception as e:
    print(e)
