import numpy as np
import random as rnd
from numpy import linalg as LA

def create_matrix(max_num: int, size: int):
    result = np.random.randint(max_num, size=(size, size))
    
    return result

def create_empty_matrix(size: int, empty=True):

    if empty == True:
        return np.zeros((size, size))
    else:
        matrix = np.zeros((size, size))
        for i in range(size):
            matrix[i][i] = 1

        return matrix

def create_vector(max_num: int, size: int):
    return np.random.randint(max_num, size=(size, 1))

def inv_matrix(matrix):
    try:
        result = LA.inv(matrix)
    except Exception:
        print("Исходная матрица необратима")
        result = None

    return result

def mul_matrix(m1, m2):
    return np.matmul(m1, m2)

def simple_multiply(array, col, q_matrix):
    res = create_empty_matrix(len(array[0]))
    n = len(array[0])

    for i in range(n):
        for j in range(n):
            temp_1 = q_matrix[i][i] * array[i][j]
            temp_2 = q_matrix[i][col] * array[col][j]
            res[i][j] = temp_1 + temp_2 * (not (col == i))

    return res
    
def l_change(l_vector, num: int):
    l_vector[num] = -1
    return l_vector

def ll_count(num1: int, num2):
    print(f'num1: {num1}')
    temp = ((-1) / num1) * num2
    return temp

def get_q(size: int, num, vector):
    q_matrix = create_empty_matrix(size, empty=False)

    for i in range(len(vector)):
        q_matrix[i][num] = vector[i]

    return q_matrix

def main():
    max_num = int(input("Введите максимальное число, которое может содержать матрица: "))
    # max_num = 1
    n = int(input("Введите размер матрицы: "))
    # n = 3
    col = int(input("Номер столбца: "))
    # col = 3

    matrix = create_matrix(max_num, n)
    inv_m = inv_matrix(matrix)

    if inv_m is not None:

        x_vector = create_vector(max_num, n)
        l_vector = mul_matrix(inv_m, x_vector)

        print(f"Исходная матрица: \n{matrix}\n")
        print(f"Инвертированная матрица: \n{inv_m}\n")
        print(f"X вектор: \n{x_vector}\n")
        print(f"L вектор: \n{l_vector}\n")

        if l_vector[col-1] != 0:

            l_wave_vector = l_change(x_vector, col-1)
            #Count result matrix
            l_hat_vector = ll_count(l_vector[col-1], l_wave_vector)
            q_matrix = get_q(n, col-1, l_hat_vector)
            print(f"Q матрица: \n{q_matrix}\n")
            result = simple_multiply(inv_m, col-1, q_matrix)
            print(f'{result}\n')
            print(mul_matrix(q_matrix, inv_m))

        else:
            print("Матрица необратима")


if __name__ == "__main__":
    main()