## 1. На вход подаётся обычная целевая функция 
## 2. (М) - количество несвободных переменных
## 3. Вводим М строк-ограничений для решения задачи оптимизации 
## 4. Далее мы парсим это в исходные данные и начинаем симплекс-метод

## 4.1 cT - вектор коэффициентов свободных членов из целевой функции
## 4.2 xT - вектор переменных x 
## 4.3 A - матрица коэффициентов при переменных в ограничениях задачи (распарсить из введённых ограничений)
## 4.4 Далее делаем вектор xT, размерности n + m. И заполняем его нулями до вектора начала размера вектора В. 
## 4.5 Делаем вектор B размера M, где лежат Ji - i это цифры из вектора xT, не равные нулю. Ji = num, где num индекс по которому лежит это число

## Алгоритм
## 1. Создаём базисную матрицу Ab, заполняем столбцами из матрицы А, индексы столбцов берём из B.

import numpy
from numpy import linalg as LA


def string_parser(s, N, M):
    sign = 1
    numb = 0
    place = 0
    it_numb = True
    answer = [0] * (N + M)
    for ch in s:
        if ch == '-':
            if place > 0:
                place = place - 1
            if not (numb == 0):
                answer[place] = numb * sign
            else:
                answer[place] = 1 * sign
            sign = -1
            it_numb = True
            numb = 0
            place = 0
        elif ch == '+':
            if place > 0:
                place = place - 1
            if not (numb == 0):
                answer[place] = numb * sign
            else:
                answer[place] = 1 * sign
            it_numb = True
            sign = 1
            place = 0
            numb = 0
        elif ch == 'x':
            it_numb = False
        elif it_numb:
            numb = numb * 10 + int(ch)
        else:
            place = place * 10 + int(ch)
    if place > 0:
        place = place - 1
    if not (numb == 0):
        answer[place] = numb * sign
    else:
        answer[place] = 1 * sign

    return numpy.array(answer)


def inp_objective_function():
    print("Enter your objective function. Example: x1 - 3x2 + 10x3 - x4")
    inp_string = input('objective function: ')
    # inp_string = 'x1+x2'
    inp_string = inp_string.replace(' ', '')
    return string_parser(inp_string, inp_string.count('x'), 0)


def inp_restrictions(N):
    l = int(input("Are we solving the M-problem? If yes, enter the number of artificial variables entered, otherwise "
                  "enter 0: "))
    #l = 0

    M = int(input("Enter number of restrictions(m):"))

    # M = 3

    print("Enter your restrictions. Example: x1 - 3x2 + 10x5 = 10")
    arr = list()

    b = list()

    # input_strings = [
    #     '-x1+x2+x3=1',
    #     'x1+x4=3',
    #     'x2+x5=2'
    # ]

    # for inp_string in input_strings:
    #     inp_string = input('restrictions №' + str(i+1) + ': ')
    #     inp_string = inp_string.replace(' ', '')
    #     my_tuple = inp_string.partition('=')
    #     b.append(int(my_tuple[2]))
    #     arr.append(string_parser(my_tuple[0], N, M + l))

    for i in range(0, M):
        inp_string = input('restrictions №' + str(i+1) + ': ')
        inp_string = inp_string.replace(' ', '')
        my_tuple = inp_string.partition('=')
        b.append(int(my_tuple[2]))
        arr.append(string_parser(my_tuple[0], N, M + l))

    return numpy.array(arr), numpy.array(b), M, l


def plus_zero_cT(cT, N, M):
    arr = [0] * (N + M)
    for i in range(0, N):
        arr[i] = cT[i]

    return numpy.array(arr)


def create_xT_B(A, b, N, M, l):
    xT = [0] * (N + M + l)
    B = [0] * M
    if l == 0:
        for i in range(0, M):
            xT[-1 - i] = b[M - i - 1]
        numb = 0
        for i in range(0, len(xT)):
            if not (xT[i] == 0):
                B[numb] = i
                numb = numb + 1
        return numpy.array(xT), numpy.array(B)
    else:
        for i in range(0, l):
            xT[-1 - i] = b[M - i - 1]
        m = M - l
        for i in range(N, len(A[0]) - l):
            amount_of_1 = 0
            for j in range(0, len(A)):
                if A[j][i] == 1:
                    amount_of_1 = amount_of_1 + 1
            if amount_of_1 == 1:
                xT[i] = b[m - 1]
                m = m - 1
            if m == 0:
                break
        numb = 0
        for i in range(0, len(xT)):
            if not (xT[i] == 0):
                B[numb] = i
                numb = numb + 1

        return numpy.array(xT), numpy.array(B)


def create_Ab(A, B):
    Ab = list()
    for i in range(0, len(B)):
        help = [0] * len(B)
        Ab.append(help)
    for n in range(0, len(B)):
        for i in range(0, len(B)):
            Ab[i][n] = A[i][B[n]]

    return numpy.array(Ab)


def inv_matrix(matrix):
    try:
        result = LA.inv(matrix)
    except Exception:
        print("Исходная матрица необратима")
        result = None

    return result


def create_cBT(cT, B):
    cBT = [0] * len(B)
    for i in range(0, len(B)):
        cBT[i] = cT[B[i]]
    return numpy.array(cBT)


def create_uT(cBT, AB1):
    return numpy.matmul(cBT, AB1)


def create_deltaT(A, cT, uT):
    res = numpy.matmul(uT, A)
    res = res - cT
    return res


def find_delta1_j0(deltaT):
    delta1 = min(deltaT)
    if delta1 < 0:
        return delta1, list(deltaT).index(delta1)
    else:
        return 'xxx', 'xxx'


def find_z(AB1, A, j0):
    Aj0 = A[:, j0]
    return numpy.dot(AB1, Aj0)


def find_teta(xT, z, B):
    teta = [0] * len(B)

    for i in range(0, len(B)):
        if (z[i]) > 0:
            teta[i] = xT[B[i]] / z[i]
        else:
            teta[i] = 'x'

    return teta


def find_minteta_k(teta):
    teta_copy = teta[:]

    while 'x' in teta_copy:
        teta_copy.pop(
            teta_copy.index('x')
        )

    minteta = min(teta_copy)
    return minteta, teta.index(minteta)


def refresh_B(B, k, j0):
    B[k] = j0

    return B


def refresh_X(xT: list, B: list, z: list, minteta, j0: int, jstar: int):
    # XJi = XJi - teta*zi

    print(f'Minteta: {minteta}, B: {B}, xT: {xT}, z: {z}')

    for i in range(len(B)):
        print(f'minteta: {minteta} * z: {z}')
        xT[B[i]] = xT[B[i]] - minteta * z[i]

    xT[j0] = minteta
    xT[jstar] = 0
    print(f'new_xT: {xT}')

    return xT


def count_simplex(cT, N, A, b, M, l):
    print(f'cT matrix: {cT}')
    print(f'A matrix: {A}')
    print(f'B matrix: {b}')
    xT, B = create_xT_B(A, b, N, M, l)
    print(f'B matrix: {B}')
    n = 1

    while True:
        print(f'Iteration №{n}')
        print(f'xT matrix: {xT}')
        Ab = create_Ab(A, B)
        print(f'Ab matrix: {Ab}')
        Ab1 = inv_matrix(Ab)
        print(f'Inverted Ab: {Ab1}')

        cbT = create_cBT(cT, B)
        print(f'cbT result: {cbT}')

        uT = create_uT(cbT, Ab1)
        print(f'uT result: {uT}')

        delta_T = create_deltaT(A, cT, uT)
        print(f'delta_t result: {delta_T}')

        if min(delta_T) > 0:
            break

        del_j, del_j_index = find_delta1_j0(delta_T)

        if del_j == 'xxx':
            return xT
        else:
            z = find_z(Ab1, A, del_j_index)

        minteta, k = find_minteta_k(
            find_teta(xT, z, B)
        )

        kk = B[k]
        B = refresh_B(B, k, del_j_index)
        xT = refresh_X(xT, B, z, minteta, del_j_index, kk)
        n = n + 1


    return xT

#9x1+6x2+7x3
#6x1+2x2+5x3+x4=180
#2x2+4x3+x5=60
#5x1+2x2+5x3+x6=120

if __name__ == "__main__":
    cT = inp_objective_function()
    N = len(cT)
    A, b, M, l = inp_restrictions(N)
    cT = plus_zero_cT(cT, N, M + l)

    result = count_simplex(cT, N, A, b, M, l)
    print(f'Result of optimization: {result}')
