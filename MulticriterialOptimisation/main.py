import matplotlib.pyplot as plt
import numpy as np
import random

# random.seed(3)
LETTERS = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
CRITERION = {0: 'Cost', 1: 'Cost of service', 2: 'Memory', 3: 'Screen'}


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
        self.CriteriaVectorNormalized = [x / sum(criteria_vector) for x in criteria_vector]    # нормализованный

        self.Alternatives = np.array([[3, 7, 6, 7],  # компьютер
                                      [4, 6, 5, 6],  # ноутбук
                                      [7, 4, 4, 5],  # планшет
                                      [5, 1, 5, 4]])  # смартфон
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
        pass

    def hierarchy(self):
        pass

mc = MultiCriteria()
# mc.criteria_to_limitation(2)
mc.pareto(1, 3)
