import numpy as np

ALPHA = 0.5
MATRIX = np.array([[6, 17, 16, 18, 15],
                   [18, 8, 16, 8, 8],
                   [6, 13, 18, 4, 3],
                   [15, 14, 2, 18, 19]])


def print_matrix(matrix=MATRIX):
    header = [f"b{i + 1}" for i in range(matrix.shape[1])]
    print("{: >10}".format("Strategies"), end="")
    for col_name in header:
        print("{: >6}".format(col_name), end="")
    print()
    for i in range(matrix.shape[0]):
        print("{: >10}".format(f"a{i + 1}"), end="")
        for j in range(matrix.shape[1]):
            print("{: >6}".format(matrix[i, j]), end="")
        print()


def print_column(column):
    for i in range(len(column)):
        print("{: >3}".format(f"a{i + 1}"), end="")
        print("{: >8}".format(column[i]), end="")
        print()
    print(f'The most suitable way is a{column.index(max(column)) + 1}: {max(column)}')


# критерий Бернулли
def bernully(matrix=MATRIX):
    print("\n\nBernully's criterion\n")
    print(f'All nature conditions have same probability: {round(1/matrix.shape[1], 2)}')
    result_vars = [round(sum(matrix[i])*(1/matrix.shape[1]), 2) for i in range(matrix.shape[0])]
    print_column(result_vars)


# пессимистический
def pessimistic(matrix=MATRIX):
    print("\n\nPessimistic criterion\n")
    result_vars = [min(matrix[i]) for i in range(matrix.shape[0])]
    print_column(result_vars)


# оптимистический
def optimistic(matrix=MATRIX):
    print("\n\nOptimistic criterion\n")
    result_vars = [max(matrix[i]) for i in range(matrix.shape[0])]
    print_column(result_vars)


# критерий Гурвица
def gurwic(matrix=MATRIX):
    print("\n\nGurwic's criterion\n")
    print(f'Probability of success is {ALPHA}')
    result_vars = [(round(ALPHA * min(matrix[i]) + (1 - ALPHA) * max(matrix[i]), 2)) for i in range(matrix.shape[0])]
    print_column(result_vars)


# критерий Саведжа
def savage(matrix=MATRIX):
    print("\n\nSavage's criterion\n")
    matrix_of_risks = np.zeros(matrix.shape)
    for j in range(matrix.shape[1]):
        maximal = matrix[0, j]
        for i in range(1, matrix.shape[0]):
            if matrix[i, j] > maximal:
                maximal = matrix[i, j]
        for i in range(0, matrix.shape[0]):
            matrix_of_risks[i, j] = maximal - matrix[i, j]
    print('Matrix of risks:')
    print_matrix(matrix_of_risks)
    result_vars = [max(matrix_of_risks[i]) for i in range(matrix.shape[0])]
    for i in range(len(result_vars)):
        print("{: >3}".format(f"a{i + 1}"), end="")
        print("{: >8}".format(result_vars[i]), end="")
        print()
    print(f'The most suitable way is a{result_vars.index(min(result_vars)) + 1}: {min(result_vars)}')



print_matrix()
bernully()
pessimistic()
optimistic()
gurwic()
savage()
