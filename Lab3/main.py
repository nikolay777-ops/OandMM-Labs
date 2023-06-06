import numpy
from numpy import linalg as LA


#lab3 functions
def fix_b(A: list, b: list):
    for i in range(len(b)):
        if b[i] < 0:
            b[i] = b[i] * -1
            for j in range(len(A[i])):
                A[i][j] = A[i][j] * -1
    return A, b


def create_newcT(N: int, M: int):
    newcT = [0] * N + [-1] * M
    return numpy.array(newcT)


def create_newA(A: list, M: int):
    newA = list()
    for i in range(len(A)):
        help = list(A[i])
        zeroone = [0] * M
        zeroone[i] = 1
        help.extend(zeroone)
        newA.append(help)
    return numpy.array(newA)


def create_xT_B(N, M, b):
    xT = [0] * (N + M)
    B = [0] * M
    for i in range(M):
        xT[i + N] = b[i]
        B[i] = i + N
    return numpy.array(xT), numpy.array(B)


def check_resxT(xT: list):
    if len(list(filter(None, xT))) > 0:
        print('Task is not compatible')
        exit()


def create_xT_after_sol(xT: list, size: int):
    newxT = [0] * size
    for i in range(size):
        newxT[i] = xT[i]
    return newxT


def check_B(B: list, size: int):
    for i in B:
        if i > size - 1:
            return False
    return True


def find_k_i_newB_in_B(B: list, size: int):
    help = list()
    for i in B:
        if i > size - 1:
            help.append(i)
    copy_B = list(B[:])
    k = copy_B.index(max(help))
    i = max(help) - size
    return k, i, copy_B


def cut(A: list, Ab1: list, newA: list,b: list, B: list, k: int, I: int, size: int):
    j = [i for i in range(size - 1)]
    for i in range(len(B)):
        if(B[i] < size):
            j.pop(j.index(B[i]))
    l = list()
    for i in j:
        l.append(numpy.matmul(Ab1, newA[:, i]))
    for i in range(len(l)):
        if not(l[i][k] == 0):
            B[k] = i
            return A, newA, b, B
    A = list(A)
    A.pop(I)
    newA = list(newA)
    newA.pop(I)
    b = list(b)
    b.pop(I)
    B = list(B)
    B.pop(k)
    return A, newA, b, B


#lab2 functions
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
    #     # inp_string = input('restrictions №' + str(i+1) + ': ')
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
    print(f'B after refresh: {B}')
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
    xT, B = create_xT_B(len(cT) - M, M, b)
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
            return xT, B, Ab1
        else:
            z = find_z(Ab1, A, del_j_index)

        minteta, k = find_minteta_k(
            find_teta(xT, z, B)
        )

        kk = B[k]
        B = refresh_B(B, k, del_j_index)
        xT = refresh_X(xT, B, z, minteta, del_j_index, kk)
        n = n + 1


    return xT, B, Ab1

if __name__ == "__main__":
    cT = inp_objective_function()
    N = len(cT)
    A, b, M, l = inp_restrictions(N)
    A, b = fix_b(A, b)
    newcT = create_newcT(len(A[0]), M)
    newA = create_newA(A, M)
    result, B, Ab1 = count_simplex(newcT, N, newA, b, M, l)
    print(f'result of simplex method = {result}')
    size = len(A[0])
    check_resxT(result[size:])
    xT = create_xT_after_sol(result, size)
    while not(check_B(B, size)):
        k, i, B = find_k_i_newB_in_B(B, size)
        A, newA, b, B = cut(A, Ab1, newA, b, B, k, i, size)
    print(f'Basic feasible plan\nx: {xT}, result B: {B}')


#x1
#0
#2
#x1 + x2 + x3 = 0
#2x1 + 2x2 + 2x3 = 0

#x1 + x2
#0
#3
#-x1 + x2 + x3 = 1
#x1 + x4 = 3
#x2 + x5 = 2

#9x1 + 6x2 + 7x3
#0
#3
#6x1 + 2x2 + 5x3 + x4 = 180
#2x2 + 4x3 + x5 = 60
#5x1 + 2x2 + 5x3 + x6 = 120

#2x1 + 3x2 + 4x3
#0
#2
#x1 + x2 + x3 + x4 = 10
#2x1 + x2 + 3x3 + x5 = 25