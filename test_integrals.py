import integrals


def func_1(x):
    return 5 * pow(x, 2) + 3 * x + 6


def func_2(x, y):
    return 5 * pow(x, 2) * pow(y, 2) + 3 * x * y + 6


print(integrals.gauss_1d_1p(func_1))
print(integrals.gauss_1d_2p(func_1))
print(integrals.gauss_1d_3p(func_1))

print('\n')

print(integrals.gauss_2d_1p(func_2))
print(integrals.gauss_2d_2p(func_2))
print(integrals.gauss_2d_3p(func_2))

print('\n')

a = -1
b = 1

print(integrals.rect_method(func_1, a, b, 5))
print(integrals.rect_method(func_1, a, b, 10))
print(integrals.rect_method(func_1, a, b, 20))
print(integrals.rect_method(func_1, a, b, 50))
