from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np


@dataclass
class Node:
    x: float
    y: float
    BC: bool = False


class JacobiMatrix:
    J: np.ndarray
    J1: np.ndarray
    detJ: float

    def __init__(self, xi_derivatives_values: List[float], eta_derivatives_values: List[float],
                 x_list: List[float], y_list: List[float]):
        dx_dxi = sum(xi * x for xi, x in zip(xi_derivatives_values, x_list))
        dy_dxi = sum(xi * y for xi, y in zip(xi_derivatives_values, y_list))
        dx_deta = sum(eta * x for eta, x in zip(eta_derivatives_values, x_list))
        dy_deta = sum(eta * y for eta, y in zip(eta_derivatives_values, y_list))

        self.J = np.array([[dx_dxi, dy_dxi], [dx_deta, dy_deta]])
        self.J1 = np.array([[dy_deta, -dy_dxi], [-dx_deta, dx_dxi]])
        self.detJ = dx_dxi * dy_deta - dy_dxi * dx_deta

        if self.detJ == 0:
            raise ValueError("Wyznacznik macierzy J jest rowny 0")


@dataclass
class Element:
    id: List[int]
    jacobi_matrices: List[JacobiMatrix] = field(default_factory=list)
    H_matrices: List[np.ndarray] = field(default_factory=list)
    integrated_H_matrix: np.ndarray = field(default_factory=lambda: np.zeros((4, 4)))
    Hbc_matrix: np.ndarray = field(default_factory=lambda: np.zeros((4, 4)))
    P_vector: np.ndarray = field(default_factory=lambda: np.zeros((4, 1)))
    C_matrices: List[np.ndarray] = field(default_factory=list)
    integrated_C_matrix: np.ndarray = field(default_factory=lambda: np.zeros((4, 4)))

    def __post_init__(self):
        self._data = {
            "H_matrices": self.H_matrices,
            "C_matrices": self.C_matrices,
            "integrated_H_matrix": self.integrated_H_matrix,
            "integrated_C_matrix": self.integrated_C_matrix,
        }

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        else:
            raise KeyError(f"Unknown key: {key}")

    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key] = value
            setattr(self, key, value)
        else:
            raise KeyError(f"Unknown key: {key}")


@dataclass
class Grid:
    nN: int
    nE: int
    elements: List[Element]
    nodes: List[Node]
    aggregated_H_matrix: np.ndarray = field(init=False)
    aggregated_P_vector: np.ndarray = field(init=False)
    aggregated_C_matrix: np.ndarray = field(init=False)

    def __post_init__(self):
        self.aggregated_H_matrix = np.zeros((self.nN, self.nN))
        self.aggregated_P_vector = np.zeros((self.nN, 1))
        self.aggregated_C_matrix = np.zeros((self.nN, self.nN))

    def __getitem__(self, key):
        if key == 'aggregated_H_matrix':
            return self.aggregated_H_matrix
        elif key == 'aggregated_C_matrix':
            return self.aggregated_C_matrix
        else:
            raise KeyError(f"Unknown key: {key}")

    def __setitem__(self, key, value):
        if key == 'aggregated_H_matrix':
            self.aggregated_H_matrix = value
        elif key == 'aggregated_C_matrix':
            self.aggregated_C_matrix = value
        else:
            raise KeyError(f"Unknown key: {key}")


@dataclass
class GlobalData:
    simulationTime: int
    simulationStepTime: int
    conductivity: int
    alfa: int
    tot: int
    initialTemp: int
    density: int
    specificHeat: int
    nN: int
    nE: int


class ElemUniv:
    dN_dxi = []
    dN_deta = []

    def __init__(self, points: List[Tuple[float, float]]):
        for point in points:
            self.dN_dxi.append(
                [-0.25 * (1 - point[1]), 0.25 * (1 - point[1]), 0.25 * (1 + point[1]), -0.25 * (1 + point[1])])
            self.dN_deta.append(
                [-0.25 * (1 - point[0]), -0.25 * (1 + point[0]), 0.25 * (1 + point[0]), 0.25 * (1 - point[0])])
