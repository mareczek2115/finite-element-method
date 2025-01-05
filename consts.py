import math

sqrt_3_5 = math.sqrt(3 / 5)

# Integration points for 2D elements
INTEGRATION_POINTS_2D = [
    (-sqrt_3_5, -sqrt_3_5), (0, -sqrt_3_5), (sqrt_3_5, -sqrt_3_5),
    (-sqrt_3_5, 0), (0, 0), (sqrt_3_5, 0),
    (-sqrt_3_5, sqrt_3_5), (0, sqrt_3_5), (sqrt_3_5, sqrt_3_5)
]

# Weights corresponding to the integration points in 2D elements
WEIGHTS_2D = [[5 / 9, 8 / 9, 5 / 9]] * 3

# Integration points for 1D boundaries of 2D elements
INTEGRATION_POINTS_1D = {
    "top": [(-sqrt_3_5, 1), (0, 1), (sqrt_3_5, 1)],
    "bottom": [(-sqrt_3_5, -1), (0, -1), (sqrt_3_5, -1)],
    "left": [(-1, sqrt_3_5), (-1, 0), (-1, -sqrt_3_5)],
    "right": [(1, sqrt_3_5), (1, 0), (1, -sqrt_3_5)]
}

# Weights corresponding to the integration points for 1D boundaries
WEIGHTS_1D = [5 / 9, 8 / 9, 5 / 9]


# sqrt_3 = math.sqrt(3)
# sqrt_3_5 = math.sqrt(3 / 5)
#
# INTEGRATION_POINTS_2D = [
#     (-1 / sqrt_3, -1 / sqrt_3), (1 / sqrt_3, -sqrt_3),
#     (-1 / sqrt_3, sqrt_3), (1 / sqrt_3, 1 / sqrt_3)
# ]
#
# WEIGHTS_2D = [[1, 1], [1, 1]]
#
# INTEGRATION_POINTS_1D = {
#     "top": [(-1 / sqrt_3, 1), (1 / sqrt_3, 1)],
#     "bottom": [(-1 / sqrt_3, -1), (1 / sqrt_3, -1)],
#     "left": [(-1, 1 / sqrt_3_5), (-1, -1 / sqrt_3_5)],
#     "right": [(1, 1 / sqrt_3_5), (1, -1 / sqrt_3_5)]
# }
#
# WEIGHTS_1D = [1, 1]


# sqrt_6_5 = math.sqrt(6/5)
# sqrt_3_7_plus = math.sqrt(3/7 + 2/7 * sqrt_6_5)
# sqrt_3_7_minus = math.sqrt(3/7 - 2/7 * sqrt_6_5)

# INTEGRATION_POINTS_2D = [
#     (-sqrt_3_7_plus, -sqrt_3_7_plus),
#     (-sqrt_3_7_minus, -sqrt_3_7_plus),
#     (sqrt_3_7_minus, -sqrt_3_7_plus),
#     (sqrt_3_7_plus, -sqrt_3_7_plus),
#     (-sqrt_3_7_plus, -sqrt_3_7_minus),
#     (-sqrt_3_7_minus, -sqrt_3_7_minus),
#     (sqrt_3_7_minus, -sqrt_3_7_minus),
#     (sqrt_3_7_plus, -sqrt_3_7_minus),
#     (-sqrt_3_7_plus, sqrt_3_7_minus),
#     (-sqrt_3_7_minus, sqrt_3_7_minus),
#     (sqrt_3_7_minus, sqrt_3_7_minus),
#     (sqrt_3_7_plus, sqrt_3_7_minus),
#     (-sqrt_3_7_plus, sqrt_3_7_plus),
#     (-sqrt_3_7_minus, sqrt_3_7_plus),
#     (sqrt_3_7_minus, sqrt_3_7_plus),
#     (sqrt_3_7_plus, sqrt_3_7_plus)
# ]
#
# sqrt_30 = math.sqrt(30)
# weight = (18 - sqrt_30) / 36, (18 + sqrt_30) / 36
#
# WEIGHTS_2D = [list(weight) * 2] * 4
#
# INTEGRATION_POINTS_1D = {
#     "top": [(-sqrt_3_7_plus, 1), (-sqrt_3_7_minus, 1), (sqrt_3_7_minus, 1), (sqrt_3_7_plus, 1)],
#     "bottom": [(-sqrt_3_7_plus, -1), (-sqrt_3_7_minus, -1), (sqrt_3_7_minus, -1), (sqrt_3_7_plus, -1)],
#     "left": [(-1, sqrt_3_7_plus), (-1, sqrt_3_7_minus), (-1, -sqrt_3_7_minus), (-1, -sqrt_3_7_plus)],
#     "right": [(1, sqrt_3_7_plus), (1, sqrt_3_7_minus), (1, -sqrt_3_7_minus), (1, -sqrt_3_7_plus)]
# }
#
# WEIGHTS_1D = [list(weight) * 2]
