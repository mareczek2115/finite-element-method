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

    integration_points = [(-1 / math.sqrt(3), -1 / math.sqrt(3)), (1 / math.sqrt(3), -1 / math.sqrt(3)),
                          (1 / math.sqrt(3), 1 / math.sqrt(3)), (-1 / math.sqrt(3), 1 / math.sqrt(3))]

    elem_univ = structs.ElemUniv(integration_points)

    for element in elements:
        element_nodes_cords = [nodes[element_node - 1] for element_node in element.id]
        x_coords = [node.x for node in element_nodes_cords]
        y_coords = [node.y for node in element_nodes_cords]

        for i in range(len(integration_points)):
            matrix = structs.JacobiMatrix(elem_univ.dN_dxi[i], elem_univ.dN_deta[i], x_coords, y_coords)
            element.jacobi_matrices.append(matrix)

    for i, element in enumerate(elements):
        print(f"element {i}\n")
        for j, matrix in enumerate(element.jacobi_matrices):
            print(f"PUNKT CALKOWANIA {j + 1}, J:")
            print(pd.DataFrame(matrix.J), f"\n\ndetJ: {matrix.detJ}, J1:")
            print(pd.DataFrame(matrix.J1), "\n\n1/detJ * J1: ")
            print(pd.DataFrame((1 / matrix.detJ) * np.array(matrix.J1)), "\n")
        print("\n")

except Exception as e:
    print(e)
