# pip install numpy
import numpy as np


# проверка оптимальности плана
def optimal_check(table, m, n, maximize=True):
    is_optimal = True
    if maximize:
        for j in range(n - 1):
            if table[m - 1, j] < 0:
                is_optimal = False
                break
    else:
        for j in range(n - 1):
            if table[m - 1, j] > 0:
                is_optimal = False
                break

    return is_optimal


def negative_in_b(table, m, n):
    has_negative = False
    for i in range(m-1):
        if table[i, n-1] < 0:
            has_negative = True
            break

    return has_negative


def find_main_row_b(table, m, n):
    row = 0
    for i in range(m - 1):
        if table[i, n-1] < 0:
            row = i
            break
    for i in range(row, m - 1):
        if table[i, n-1] < 0 and table[i, n-1] < table[row, n-1]:
            row = i

    return row


def find_main_column_b(table, m, n, main_row):
    column = 0
    for j in range(n - 1):
        if table[main_row, j] < 0:
            column = j
            break
    for j in range(n - 1):
        if (table[main_row, j] < 0 and table[main_row, n - 1] / table[main_row, j] < table[main_row, n - 1] /
                table[main_row, column]):
            column = j

    return column


# поиск разрешающего столбца
def find_support_column(table, m, n, maximize=True):
    column = 0
    for j in range(n-1):
        if maximize and table[m-1, j] < table[m-1, column]:
            column = j
        elif not maximize and table[m-1, j] > table[m-1, column]:
            column = j

    return column


# поиск разрешающей строки
def find_support_row(table, m, n, support_column, maximize=True):
    row = 0
    for i in range(m - 1):
        if table[i, support_column] > 0:
            row = i
            break
    for i in range(row, m - 1):
        if (table[i, support_column] > 0) and ((table[i, n-1] / table[i, support_column]) < (table[row, n-1] / table[row, support_column])):
            row = i

    return row


def find_result(table, m, n):
    result = np.zeros(n-1)
    for i in range(m-1):
        for j in range(n-1):
            if table[i, j] == 1:
                s = 0
                for k in range(m-1):
                    s += table[k, j]
                if s == 1:
                    result[j] = table[i, n-1]
    return result


def refill_table(table, m, n, support_row, support_column):
    new_table = np.zeros((m, n))
    for j in range(n):
        # в разрешающей строке все элементы делим на разрешающий элемент
        new_table[support_row, j] = table[support_row, j] / table[support_row, support_column]
    for i in range(m):
        if i == support_row:
            continue
        for j in range(n):
            # пересчет остальных строк (из строки вычитаем разрешающую строку, умноженную на соответствующий элемент
            # разрешающего столбца
            new_table[i, j] = table[i, j] - table[i, support_column] * new_table[support_row, j]
    # пересчет строки переменных
    result = find_result(table, m, n)

    return new_table, result


def print_info(table, result, func):
    print('Table:')
    print(table)
    print(f'Solution: {result}')
    s = 0
    # получение значения функции в полученном плане
    for i in range(len(result)):
        s += -func[i] * result[i]
    print(f'Value of target function: {s}')
    print()


def simplex(a, b, c, maximize=True):
    m, n = a.shape

    # создание симплекс-таблицы
    if maximize: # для поиска максимума в таблицу с противоположным знаком добавляется только сама функция
        A = a
        B = b
        C = np.array([-x for x in c])
    else: # для минимизации с противоположным знаком добавляются все матрицы
        A = np.array([-x for x in a])
        B = np.array([-x for x in b])
        C = np.array([-x for x in c])

    table = np.hstack((A, np.eye(m))) # добавление фиктивных переменных
    table = np.insert(table, table.shape[1], B, axis=1)
    for i in range(table.shape[1] - n):
        C = np.append(C, 0)

    table = np.vstack([table, C])

    m, n = table.shape # изменение значений размеров

    print(table)

    # необходимо, чтобы в столбце базисных переменных не было отрицательных элементов
    while negative_in_b(table, m, n):
        # поиск разрешающих строки и столбца
        main_row = find_main_row_b(table, m, n)
        main_column = find_main_column_b(table, m, n, main_row)
        # пересчет значений в новом базисе
        table, result = refill_table(table, m, n, main_row, main_column)
        print_info(table, result, C)

    # меняем базис пока план не станет оптимальным
    while not optimal_check(table, m, n, maximize):
        print(f'Plan {table[m-1, :-1]} is not optimal. Changing of basis\n')
        # поиск разрешающих строки и столбца
        support_column = find_support_column(table, m, n, maximize)
        support_row = find_support_row(table, m, n, support_column, maximize)
        # пересчет значений в новом базисе
        table, result = refill_table(table, m, n, support_row, support_column)

        print_info(table, result, C)

    print(f'Plan {table[m-1, :-1]} is optimal')
    result = find_result(table, m, n)
    s = 0
    for i in range(len(result)):
        s += -C[i] * result[i]
    if maximize:
        print(f'Maximal value of function is {s}')
    else:
        print(f'Minimal value of function is {s}')


# входные данные
c = np.array([1, 4])
A = np.array([[3, 2],
              [1, 2]])
b = np.array([12, 8])

# для прямой задачи
simplex(A, b, c)

# для двойственной задачи
simplex(A.T, c.T, b.T, maximize=False)