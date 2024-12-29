import sys
import pandas as pd

from structs import GlobalData, Grid, ElemUniv
from consts import INTEGRATION_POINTS_H, WEIGHTS_H, INTEGRATION_POINTS_HBC, WEIGHTS_HBC
from parse_file import read_file
from matrix_operations import calculate_H_matrices, integrate_H_matrices, aggregate_H_matrices, calculate_Hbc_matrices
from vectors import calculate_P_vector, aggregate_P_vectors


file_name = sys.argv[1] if len(sys.argv) > 1 else None

try:
    if not file_name:
        raise FileNotFoundError("Podaj nazwe pliku, z ktorego chcesz wczytac dane, jako argument")

    elements, nodes, field_values = read_file(file_name)

    data = GlobalData(*field_values[:10])
    grid = Grid(nN=field_values[-2], nE=field_values[-1], elements=elements, nodes=nodes)

    elem_univ = ElemUniv(INTEGRATION_POINTS_H)

    calculate_H_matrices(grid, elem_univ, data.conductivity)
    integrate_H_matrices(elements, WEIGHTS_H, INTEGRATION_POINTS_H)
    aggregate_H_matrices(grid)

    calculate_Hbc_matrices(data, grid, WEIGHTS_HBC, INTEGRATION_POINTS_HBC)
    calculate_P_vector(data, grid, WEIGHTS_HBC, INTEGRATION_POINTS_HBC)
    aggregate_P_vectors(grid)

    # grid.t_vector = -1 * np.linalg.inv(grid.aggregated_H_matrix) * grid.aggregated_P_vector
    # print(pd.DataFrame(grid.t_vector))


except ValueError as e:
    print(f"Value Error: {e}")
except FileNotFoundError as e:
    print(f"File Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
