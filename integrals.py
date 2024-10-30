import math


def gauss_integration_1d(f, points, weights):
    return sum(w * f(x) for x, w in zip(points, weights))


def gauss_1d_1p(f):
    return gauss_integration_1d(f, points=[0], weights=[2])


def gauss_1d_2p(f):
    points = [-1 / math.sqrt(3), 1 / math.sqrt(3)]
    return gauss_integration_1d(f, points=points, weights=[1, 1])


def gauss_1d_3p(f):
    points = [-math.sqrt(3 / 5), 0, math.sqrt(3 / 5)]
    weights = [5 / 9, 8 / 9, 5 / 9]

    return gauss_integration_1d(f, points=points, weights=weights)


def gauss_integration_2d(f, points, weights):
    result = 0
    for ksi in points:
        for eta in points:
            result += f(ksi, eta) * weights[points.index(ksi)] * weights[points.index(eta)]

    return result


def gauss_2d_1p(f):
    return gauss_integration_2d(f, points=[0], weights=[2])


def gauss_2d_2p(f):
    points = [-1 / math.sqrt(3), 1 / math.sqrt(3)]
    return gauss_integration_2d(f, points=points, weights=[1, 1])


def gauss_2d_3p(f):
    points = [-math.sqrt(3 / 5), 0, math.sqrt(3 / 5)]
    weights = [5 / 9, 8 / 9, 5 / 9]

    return gauss_integration_2d(f, points=points, weights=weights)


def rect_method(f, a, b, n):
    dx = (b - a) / n

    return sum(f(a + i * dx) * dx for i in range(n))
