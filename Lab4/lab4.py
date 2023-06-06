import numpy

from lab3 import *


def add_zeros_to_cT(cT: list, amount: int):
    return list(cT) + [0] * amount


def find_kB_kT(Ab1: list, b: list, B: list, size: int):
    kT = [0] * size
    kB = numpy.matmul(Ab1, b)
    for i in range(len(B)):
        kT[B[i]] = kB[i]
    return kB, kT


def contains_negative(numbers: list):
    for num in numbers:
        if num < 0:
            return True
    return False


def find_j_index(kT: list, B: list):
    for i in range(len(kT)):
        if kT[i * (-1) - 1] < 0:
            return list(B).index(len(kT) - i - 1)


def find_nu(delta_yT: list, A: list, B: list):
    size = len(A[0])
    nu = [0] * size
    j = [i for i in range(size - 1)]
    index = [item for item in j if item not in B]
    for i in index:
        nu[i] = numpy.matmul(delta_yT, A[:, i])
    return nu, index


def find_j0_from_sigma(cT: list, A: list, yT: list, nu: list, index: list):
    sigma = list()
    A = numpy.array(A)
    y = numpy.transpose(yT)
    for i in index:
        if nu[i] < 0:
            sigma.append((cT[i] - numpy.matmul(numpy.transpose(A[:, i]), y)) / nu[i])
    print(f'sigma: {sigma}')
    if len(sigma) == 0:
        return 'x'
    else:
        return sigma.index(min(sigma))


def dual_simplex_method(cT: list, A: list, b: list, N: int, M: int, l: int, xT: list, B: list):
    iter = 1
    while True:
        print(f'Iteration №{iter}')
        Ab = create_Ab(A, B)
        print(f'Ab matrix: {Ab}')
        Ab1 = inv_matrix(Ab)
        print(f'Inverted Ab: {Ab1}')
        cbT = create_cBT(cT, B)
        print(f'cbT result: {cbT}')
        yT = create_uT(cbT, Ab1)
        print(f'yT result: {yT}')

        kB, kT = find_kB_kT(Ab1, b, B, len(cT))
        print(f'kB: {kB}')
        print(f'kT: {kT}')

        if (not (contains_negative(kT))):
            print(f'Solution: {kT}')
            exit()

        j_index = find_j_index(kT, B)
        print(f'j_index: {j_index}')

        delta_yT = Ab1[j_index]
        print(f'delta_yT: {delta_yT}')

        nu, index = find_nu(delta_yT, A, B)
        print(f'nu: {nu}')

        j0 = find_j0_from_sigma(cT, A, yT, nu, index)
        if j0 == 'x':
            print('Task is not compatible')
        else:
            print(f'j0: {j0}')

        B[j_index] = j0
        print(f'B: {B}')
        iter += 1


def main():
    cT = inp_objective_function()
    N = len(cT)
    A, b, M, l = inp_restrictions(N)
    cT = add_zeros_to_cT(cT, len(A[0]) - N)
    xT, B = create_xT_B(len(cT) - M, M, b)

    print(f'cT: {cT}')
    print(f'A: {A}')
    print(f'b: {b}')
    print(f'N: {N}')
    print(f'M: {M}')
    print(f'l: {l}')
    print(f'xT: {xT}')
    print(f'B: {B}')

    dual_simplex_method(cT, A, b, N, M, l, xT, B)

if __name__ == '__main__':
    main()

# -4x1 -3x2 - 7x3
# 0
# 2
# -2x1 -x2 -4x3 + x4 = -1
# -2x1 -2x2 -2x3 + x5 = -1.5
