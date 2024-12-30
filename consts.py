import math

# Integration points for 2D elements, defined in the reference space (ξ, η).
INTEGRATION_POINTS_2D = [(-math.sqrt(3 / 5), -math.sqrt(3 / 5)), (0, -math.sqrt(3 / 5)),
                        (math.sqrt(3 / 5), -math.sqrt(3 / 5)),
                        (-math.sqrt(3 / 5), 0), (0, 0), (math.sqrt(3 / 5), 0),
                        (-math.sqrt(3 / 5), math.sqrt(3 / 5)), (0, math.sqrt(3 / 5)),
                        (math.sqrt(3 / 5), math.sqrt(3 / 5))]
# Weights corresponding to the integration points in 2D elements.
WEIGHTS_2D = [[5 / 9, 8 / 9, 5 / 9],
             [5 / 9, 8 / 9, 5 / 9],
             [5 / 9, 8 / 9, 5 / 9]]

# Integration points for 1D boundaries of 2D elements, defined in the reference space.
INTEGRATION_POINTS_1D = {
    "top": [(-math.sqrt(3 / 5), 1), (0, 1), (math.sqrt(3 / 5), 1)],
    "bottom": [(-math.sqrt(3 / 5), -1), (0, -1), (math.sqrt(3 / 5), -1)],
    "left": [(-1, math.sqrt(3 / 5)), (-1, 0), (-1, -math.sqrt(3 / 5))],
    "right": [(1, math.sqrt(3 / 5)), (1, 0), (1, -math.sqrt(3 / 5))]
}
# Weights corresponding to the integration points for 1D boundaries
WEIGHTS_1D = [5 / 9, 8 / 9, 5 / 9]
