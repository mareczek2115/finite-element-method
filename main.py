import sys
import pandas as pd

from structs import GlobalData, Grid, ElemUniv
from consts import INTEGRATION_POINTS_2D, WEIGHTS_2D, INTEGRATION_POINTS_1D, WEIGHTS_1D
from parse_file import read_file
from matrix_operations import calculate_H_matrices, calculate_Hbc_matrices, calculate_C_matrices, \
    integrate_matrices, aggregate_matrices
from vectors import calculate_P_vector, aggregate_P_vectors


file_name = sys.argv[1] if len(sys.argv) > 1 else None

try:
    if not file_name:
        raise FileNotFoundError("Podaj nazwe pliku, z ktorego chcesz wczytac dane, jako argument")

    elements, nodes, field_values = read_file(file_name)

    data = GlobalData(*field_values[:10])
    grid = Grid(nN=field_values[-2], nE=field_values[-1], elements=elements, nodes=nodes)

    elem_univ = ElemUniv(INTEGRATION_POINTS_2D)

    calculate_H_matrices(grid, elem_univ, data.conductivity)
    integrate_matrices(elements, 'H', WEIGHTS_2D, INTEGRATION_POINTS_2D)
    aggregate_matrices(grid, 'H')

    calculate_Hbc_matrices(data, grid, WEIGHTS_1D, INTEGRATION_POINTS_1D)
    calculate_P_vector(data, grid, WEIGHTS_1D, INTEGRATION_POINTS_1D)
    aggregate_P_vectors(grid)

    calculate_C_matrices(data, grid, INTEGRATION_POINTS_2D)
    integrate_matrices(elements, 'C', WEIGHTS_2D, INTEGRATION_POINTS_2D)
    aggregate_matrices(grid, 'C')
    print(pd.DataFrame(grid.aggregated_C_matrix))
    # grid.t_vector = -1 * np.linalg.inv(grid.aggregated_H_matrix) * grid.aggregated_P_vector
    # print(pd.DataFrame(grid.t_vector))


except ValueError as e:
    print(f"Value Error: {e}")
except FileNotFoundError as e:
    print(f"File Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
