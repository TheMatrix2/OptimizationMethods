# pip install numpy
import numpy as np


class Simplex:
    def __init__(self, a, b, c, maximize=True):    # создание симплекс-таблицы
        if maximize:    # для максимизации с противоположным знаком добавляется только матрица функции
            A = a
            B = b
            C = np.array([-x for x in c])
        else:   # для поиска минимума все матрицы добавляются в таблицу с противоположным знаком
            A = np.array([-x for x in a])
            B = np.array([-x for x in b])
            C = np.array([-x for x in c])

        self.Solution = np.zeros(len(c))    # строка решения по количеству переменных в функции

        t = np.hstack((A, np.eye(A.shape[0])))  # добавление фиктивных переменных
        t = np.insert(t, t.shape[1], B, axis=1)
        for i in range(t.shape[1] - A.shape[1]):
            C = np.append(C, 0)

        self.Maximize = maximize
        self.Function = c
        self.Table = np.vstack([t, C])  # созданная таблица
        self.M, self.N = self.Table.shape   # изменение значений размеров
        self.Basis = np.zeros(self.N - 1)   # строка базиса

    def function_is_limited(self):    # проверка ограниченности функции
        lim = True
        for j in range(self.N - 1):
            for i in range(self.M - 1):
                if self.Table[i, j] / self.Table[i, self.N - 1] >= -0:
                    lim = True
                    break
                else:
                    lim = False

        return lim

    def solution_exists(self):    # проверка существования решения
        exists = True
        column = self.N - 1
        for i in range(self.M - 1):
            if self.Table[i, column] >= 0:
                continue
            else:
                exists = False
                column -= 1
                while column >= 0:
                    if self.Table[i, column] < 0:
                        exists = True
                        column = self.N - 1
                        break
                    else:
                        column -= 1

        return exists

    def check(self):
        if not self.function_is_limited():
            print('Target function is not limited')
            return False
        if not self.solution_exists():
            print("Solution does not exist")
            return False
        return True

    def solution_is_acceptable(self):   # проверка допустимости решения
        is_acceptable = True
        for i in range(self.M - 1):
            if self.Table[i, self.N - 1] < 0:
                is_acceptable = False
                break

        return is_acceptable

    def plan_is_optimal(self):  # проверка оптимальности решения
        is_optimal = True
        for j in range(self.N - 1):
            if ((self.Maximize and self.Table[self.M - 1, j] < 0) or
                    (not self.Maximize and self.Table[self.M - 1, j] > 0)):
                is_optimal = False
                break

        return is_optimal

    def support_row_b(self):    # разрешающая строка для поиска допустимого решения
        row = 0
        for i in range(1, self.M - 1):
            if self.Table[i, self.N - 1] < 0:
                row = i
                break
        for i in range(row, self.M - 1):
            if self.Table[i, self.N - 1] < self.Table[row, self.N - 1]:
                row = i

        return row

    def support_column_b(self, row):    # разрешающий столбец для поиска допустимого решения
        column = 0
        for j in range(self.N - 1):
            if self.Table[row, j] < 0:
                column = j
                break
        for j in range(self.N - 1):
            if (self.Table[row, j] < 0 and self.Table[row, self.N - 1] / self.Table[row, j] <
                    self.Table[row, self.N - 1] / self.Table[row, column]):
                column = j

        return column

    def find_support_column(self):  # разрешающий столбец для поиска оптимального решения
        column = 0
        for j in range(self.N - 1):
            if ((self.Maximize and self.Table[self.M - 1, j] < self.Table[self.M - 1, column]) or
                    (not self.Maximize and self.Table[self.M - 1, j] > self.Table[self.M - 1, column])):
                column = j

        return column

    def find_support_row(self, column):   # разрешающая строка для поиска оптимального решения
        row = 0
        for i in range(self.M - 1):
            if self.Table[i, column] != 0 and self.Table[i, self.N - 1] / self.Table[i, column] > 0:
                row = i
        for i in range(self.M - 1):
            if self.Table[i, column] != 0:
                Q = self.Table[i, self.N - 1] / self.Table[i, column]
            else:
                continue
            if (Q >= 0) and (Q < self.Table[row, self.N - 1] / self.Table[row, column]):
                row = i

        return row

    def refill_table(self, support_row, support_column, b=True):    # пересчет таблицы
        new_table = np.zeros((self.M, self.N))
        for j in range(self.N):
            # в разрешающей строке все элементы делим на разрешающий элемент
            new_table[support_row, j] = self.Table[support_row, j] / self.Table[support_row, support_column]
        for i in range(self.M):
            if i == support_row:
                continue
            for j in range(self.N):
                # пересчет остальных строк (из строки вычитаем разрешающую строку, умноженную на соответствующий
                # элемент разрешающего столбца
                new_table[i, j] = self.Table[i, j] - self.Table[i, support_column] * new_table[support_row, j]
        self.Table = new_table

    def find_solution(self):
        result = np.zeros(self.N - 1)
        basis = np.zeros(self.N - 1)
        for i in range(self.M - 1):
            for j in range(self.N - 1):
                if self.Table[i, j] == 1:
                    s = 0
                    for k in range(self.M - 1):
                        s += self.Table[k, j]
                    if s == 1:
                        basis[j] = 1
                        result[j] = self.Table[i, self.N - 1]
        self.Basis = basis
        self.Solution = result[:len(self.Function)]

    def print_info(self):
        print('Table:')
        header = [f"x{i}" for i in range(1, self.N)] + ["b"]
        print("{: >8}".format(""), end="")
        for col_name in header:
            print("{: >8}".format(col_name), end="")
        print()

        for i in range(self.M):
            print("{: >8}".format("x{}".format(i + 1)), end="")
            for j in range(self.N):
                print("{: >8.2f}".format(round(self.Table[i, j], 2)), end="")
            print()
        print(f'Basis: {self.Basis}')
        print('Solution: [ ', end="")
        for x in self.Solution:
            print(f'{round(x, 2)} ', end="")
        print(']')
        s = 0
        # получение значения функции в полученном плане
        for i in range(len(self.Solution)):
            s += -self.Function[i] * self.Solution[i]
        print(f'Value of target function: {round(s, 2)}')
        print()

    def calculate(self):
        self.print_info()
        break_flag = False
        while self.function_is_limited() and not self.solution_is_acceptable():
            print('Solution is not acceptable')
            row = self.support_row_b()
            column = self.support_column_b(row)
            self.refill_table(row, column)
            if not self.function_is_limited():
                break_flag = True
            self.find_solution()
            self.print_info()

        if not break_flag:
            count = 0
            while not self.plan_is_optimal() and self.solution_exists():
                count += 1
                print('Solution is not optimal')
                print(f'Iteration {count}')
                column = self.find_support_column()
                row = self.find_support_row(column)
                self.refill_table(row, column)
                if not self.solution_exists():
                    break
                self.find_solution()
                self.print_info()
