from dataclasses import dataclass, field
import numpy as np


@dataclass
class Node:
    x: float
    y: float


@dataclass
class JacobiMatrix:
    J: list[list[float]]
    J1: list[list[float]]
    detJ: float

    def __init__(self, xi_derivatives_values, eta_derivatives_values, x_list, y_list):
        dx_dxi = sum(xi * x for xi, x in zip(xi_derivatives_values, x_list))
        dy_dxi = sum(xi * y for xi, y in zip(xi_derivatives_values, y_list))
        dx_deta = sum(eta * x for eta, x in zip(eta_derivatives_values, x_list))
        dy_deta = sum(eta * y for eta, y in zip(eta_derivatives_values, y_list))

        self.J = [[dx_dxi, dy_dxi], [dx_deta, dy_deta]]
        self.J1 = [[dy_deta, -dy_dxi], [-dx_deta, dx_dxi]]
        self.detJ = dx_dxi * dy_deta - dy_dxi * dx_deta


@dataclass
class Element:
    id: list[int]
    jacobi_matrices: list[JacobiMatrix] = field(default_factory=list)
    H_matrices: list[np.ndarray] = field(default_factory=list)
    integrated_H_matrix: np.ndarray = field(default_factory=list)


@dataclass
class Grid:
    nN: int
    nE: int
    elements: list[Element]
    nodes: list[Node]


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


@dataclass
class ElemUniv:
    dN_dxi = []
    dN_deta = []

    def __init__(self, points: list[tuple]):
        for point in points:
            self.dN_dxi.append(
                [-0.25 * (1 - point[0]), 0.25 * (1 - point[0]), 0.25 * (1 + point[0]), -0.25 * (1 + point[0])])
            self.dN_deta.append(
                [-0.25 * (1 - point[1]), -0.25 * (1 + point[1]), 0.25 * (1 + point[1]), 0.25 * (1 - point[1])])
