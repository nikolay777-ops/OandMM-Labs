import numpy
from lab3 import *


def dual_simplex_method():
    pass


def main():
    cT = inp_objective_function()
    N = len(cT)
    A, b, M, l = inp_restrictions(N)

    print(f'cT: {cT}')
    print(f'A: {A}')
    print(f'B: {b}')
    print(f'M: {M}')
    print(f'l: {l}')


if __name__ == '__main__':
    main()

# -4x1 -3x2 - 7x3
# 0
# 2
