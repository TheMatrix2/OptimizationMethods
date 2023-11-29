import matplotlib.pyplot as plt
import numpy as np
import random

# random.seed(3)
LETTERS = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
CRITERION = {0: 'Cost', 1: 'Cost of service', 2: 'Memory', 3: 'Screen'}
ALTERNATIVES = {0: 'Computer', 1: 'Laptop', 2: 'Tablet', 3: 'Smartphone'}
RANDOM_CONSISTENCY = 0.9
N = 4


def find_max(table, criteria):
    a_max = 0
    for i in range(len(table)):
        if table[i][criteria - 1] > a_max:
            a_max = table[i][criteria - 1]
    return a_max


def find_min(table, criteria):
    a_min = 10
    for i in range(len(table)):
        if table[i][criteria - 1] < a_min:
            a_min = table[i][criteria - 1]
    return a_min


class MultiCriteria:
    def __init__(self):
        # ВЫБОР УСТРОЙСТВА ДЛЯ РАБОТЫ: компьютер, ноутбук, планшет, смартфон
        # Важность критериев. Цена - 8, обслуживание - 2, объем памяти - 4, экран - 6
        criteria_vector = [8, 2, 4, 6]
        # нормализованный
        self.CriteriaVectorNormalized = np.array([[x / sum(criteria_vector)] for x in criteria_vector])

        self.Alternatives = np.array([[3, 7, 6, 7],  # компьютер
                                      [4, 6, 5, 6],  # ноутбук
                                      [7, 4, 4, 5],  # планшет
                                      [5, 1, 5, 4]])  # смартфон
        # self.Alternatives = np.array([[1, 9, 9, 1],  # компьютер
        #                               [3, 7, 7, 3],  # ноутбук
        #                               [7, 3, 1, 7],  # планшет
        #                               [9, 1, 3, 9]])  # смартфон
        self.M, self.N = self.Alternatives.shape

    def print_table(self, table):
        print('Table:')
        header = [f"{i+1}" for i in range(self.N)]
        print("{: >8}".format(""), end="")
        for col_name in header:
            print("{: >8}".format(col_name), end="")
        print()

        for i in range(self.M):
            print("{: >8}".format(f"{LETTERS[i]}"), end="")
            for j in range(self.N):
                print("{: >8.2f}".format(table[i, j]), end="")
            print()

    # замена критериев ограничениями
    def criteria_to_limitation(self, main_criteria):
        new_table = np.zeros((self.M, self.N))
        for j in range(self.N):
            a_min = find_min(self.Alternatives, j + 1)
            a_max = find_max(self.Alternatives, j + 1)
            for i in range(self.M):
                if j == main_criteria - 1:
                    new_table[i][j] = self.Alternatives[i][j]
                else:
                    new_table[i][j] = round((self.Alternatives[i][j] - a_min) / (a_max - a_min), 2)

        limits = []
        for j in range(self.N):
            if j != main_criteria - 1:
                limits.append(random.randint(1, 5) / 10)
            else:
                limits.append(0)

        suitable_alternatives = []
        index = []
        for i in range(self.M):
            suitable = True
            for j in range(self.N):
                if j == main_criteria - 1:
                    continue
                elif new_table[i][j] >= limits[j]:
                    continue
                else:
                    suitable = False
                    break
            if suitable:
                suitable_alternatives.append(list(new_table[i]))
                index.append(i)
        self.print_table(new_table)
        print(f'Limitations: {limits}')

        if len(suitable_alternatives) == 1:
            print(f'Optimal alternative is {LETTERS[index[0]]}')
        elif len(suitable_alternatives) > 1:
            print(f'There are too many alternatives.')
            print(suitable_alternatives)
            m = find_max(suitable_alternatives, main_criteria)
            for i in range(len(suitable_alternatives)):
                if suitable_alternatives[i][main_criteria - 1] == m:
                    print(f'The most suitable is {LETTERS[index[i]]}')
        else:
            print('There is no alternatives. Change limitations')

    # формирование и сужение множества Парето
    def pareto(self, criteria1, criteria2):
        plt.scatter(self.Alternatives[criteria1 - 1], self.Alternatives[criteria2 - 1])
        for label, x, y in zip(['A', 'B', 'C', 'D'], self.Alternatives[criteria1 - 1], self.Alternatives[criteria2 - 1]):
            plt.annotate(label, xy=(x, y), xytext=(5, -5), textcoords='offset points')
        max_value = max(max(self.Alternatives[criteria1 - 1]), max(self.Alternatives[criteria2 - 1]))
        min_value = min(min(self.Alternatives[criteria1 - 1]), min(self.Alternatives[criteria2 - 1]))
        plt.scatter(max_value, max_value, marker='*', color='red', label='Utopia')
        plt.xlim(min_value - 1, max_value + 1)
        plt.ylim(min_value - 1, max_value + 1)
        plt.xlabel(CRITERION[criteria1 - 1])
        plt.ylabel(CRITERION[criteria2 - 1])
        plt.legend()
        plt.grid(True)
        plt.show()

    # взвешивание и объединение критериев
    def weighing_and_comparing(self):
        normalized_table = np.zeros((self.M, self.N))
        for j in range(self.N):
            s = 0
            for i in range(self.M):
                s += self.Alternatives[i][j]
            for i in range(self.M):
                normalized_table[i][j] = round(self.Alternatives[i][j] / s, 2)
        self.print_table(normalized_table)
        result = np.dot(normalized_table, self.CriteriaVectorNormalized)
        print(result)

    # анализ иерархий
    def hierarchy(self):
        for k in range(4):
            print(CRITERION[k])
            comparing = np.ones((self.M, self.N))
            summ_column = []
            summ_row = np.zeros(self.N)
            for i in range(self.M):
                s = 1
                m = 1
                for j in range(self.N):
                    comparing[i][j] = self.Alternatives[i][k] / self.Alternatives[j][k]
                    s *= comparing[i][j]
                    m *= comparing[i][j]
                    summ_row[j] += comparing[i][j]
                summ_column.append(pow(s, 1 / N))
            normalized_column = [x / sum(summ_column) for x in summ_column]

            header = [LETTERS[i] for i in range(self.N)] + ['Summ'] + ['nSumm']
            print("{: >8}".format(""), end="")
            for col_name in header:
                print("{: >8}".format(col_name), end="")
            print()

            for i in range(self.M):
                print("{: >8}".format(f"{LETTERS[i]}"), end="")
                for j in range(self.N):
                    print("{: >8.2f}".format(comparing[i, j]), end="")
                print("{: >8.2f}".format(summ_column[i]), end="")
                print("{: >8.2f}".format(normalized_column[i]), end="")
                print()
            print("{: >8}".format("Summ"), end="")
            for j in range(self.N):
                print("{: >8.2f}".format(summ_row[j]), end="")
            print("{: >8.2f}".format(sum(summ_column)), end="")
            print("{: >8.2f}".format(sum(normalized_column)), end="")
            print()
            print(sum(summ_row * normalized_column))
            print("\n")

mc = MultiCriteria()
# mc.criteria_to_limitation(2)
# mc.pareto(1, 3)
# mc.weighing_and_comparing()
mc.hierarchy()
