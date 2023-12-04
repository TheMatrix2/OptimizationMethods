from Simplex import *


def print_result(simplex):
    if simplex.check():
        print('Solution: [', end="")
        for x in simplex.Solution:
            print(f'{round(x, 2)} ', end="")
        print(']')
        s = 0
        # получение значения функции в полученном плане
        for i in range(len(simplex.Solution)):
            s += simplex.Function[i] * simplex.Solution[i]
        if simplex.Minimize:
            print(f'Minimal acceptable and optimal value of target function is {round(s, 2)}')
        else:
            print(f'Maximal acceptable and optimal value of target function: {round(s, 2)}')


# входные данные
C = np.array([2, 6, 7])
A = np.array([[3, 1, 1],
              [1, 2, 0],
              [0, 0.5, 2]])
B = np.array([3, 8, 1])

# для прямой задачи
print('\nDIRECT PROBLEM\n')
simplex_direct = Simplex(A, B, C)
simplex_direct.calculate()
print_result(simplex_direct)


# для двойственной задачи
print('\nDUAL PROBLEM\n')
simplex_dual = Simplex(A.T, C.T, B.T, minimize=False)
simplex_dual.calculate()
print_result(simplex_dual)
