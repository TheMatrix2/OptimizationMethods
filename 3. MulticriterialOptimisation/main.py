import matplotlib.pyplot as plt
import numpy as np
import random

# random.seed(2)
LETTERS = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
CRITERION = {0: 'Cost', 1: 'Cost of service', 2: 'Memory', 3: 'Screen', 4: 'Criteria priority'}
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

        self.Alternatives = np.array([[7, 4, 6, 7],  # компьютер
                                      [7, 5, 5, 6],  # ноутбук
                                      [3, 6, 4, 5],  # планшет
                                      [6, 7, 5, 4]])  # смартфон
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
        x = np.array([self.Alternatives[i, criteria1 - 1] for i in range(len(self.Alternatives))])
        y = np.array([self.Alternatives[i, criteria2 - 1] for i in range(len(self.Alternatives))])
        plt.scatter(x, y)
        alph = ['A', 'B', 'C', 'D']
        for label in alph:
            plt.annotate(label, xy=(0, 0), xytext=(x[alph.index(label)], y[alph.index(label)] + 0.1))
        max_value = 10
        min_value = 0
        plt.scatter(min_value if criteria1-1 == 0 or criteria1-1 == 1 else max_value,
                    min_value if criteria2-1 == 0 or criteria2-1 == 1 else max_value,
                    marker='*', color='red')
        plt.annotate('Utopia', xy=(0, 0), xytext=(min_value+0.2 if criteria1-1 == 0 or criteria1-1 == 1 else max_value+0.2,
                                                  min_value+0.2 if criteria2-1 == 0 or criteria2-1 == 1 else max_value+0.2))
        plt.xlim(-1, 11)
        plt.ylim(-1, 11)
        plt.xlabel(CRITERION[criteria1 - 1])
        plt.ylabel(CRITERION[criteria2 - 1])
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
        cost = np.array([[1, 3, 1/3, 1],
                         [0, 1, 1/5, 3],
                         [0, 0, 1, 5],
                         [0, 0, 0, 1]])
        cost_of_service = np.array([[1, 3, 3, 7],
                                    [0, 1, 1, 1/3],
                                    [0, 0, 1, 1],
                                    [0, 0, 0, 1]])
        memory = np.array([[1, 3, 5, 1/3],
                           [0, 1, 3, 1],
                           [0, 0, 1, 1/7],
                           [0, 0, 0, 1]])
        screen = np.array([[1, 1/3, 1/5, 1/7],
                           [0, 1, 1, 1/5],
                           [0, 0, 1, 1/3],
                           [0, 0, 0, 1]])
        criteria_priority = np.array([[1., 3., 5., 7.],
                                      [0., 1., 3., 5.],
                                      [0., 0., 1., 3.],
                                      [0., 0., 0., 1.]])
        tables = [cost, cost_of_service, memory, screen, criteria_priority]

        alternative_comparing = np.array(np.zeros(self.M))
        criteria_comparing = []
        for k in range(len(tables)):
            print(CRITERION[k])
            for i in range(self.M - 1, 0, -1):  # заполнение части под диагональю
                for j in range(self.N):
                    tables[k][i, j] = 1 / tables[k][j, i]
            summ_column = []
            summ_row = np.zeros(self.N)
            for i in range(self.M):
                s = 0
                m = 1
                for j in range(self.N):
                    s += tables[k][i, j]
                    m *= tables[k][i, j]
                    summ_row[j] += tables[k][i, j]
                summ_column.append(s)
            normalized_column = [x / sum(summ_column) for x in summ_column]

            header = [LETTERS[i] if k != (len(tables)-1) else i for i in range(self.N)] + ['Summ'] + ['nSumm']
            print("{: >8}".format(""), end="")
            for col_name in header:
                print("{: >8}".format(col_name), end="")
            print()

            for i in range(self.M):
                print("{: >8}".format(f"{LETTERS[i]}"), end="")
                for j in range(self.N):
                    print("{: >8.2f}".format(tables[k][i, j]), end="")
                print("{: >8.2f}".format(summ_column[i]), end="")
                print("{: >8.2f}".format(normalized_column[i]), end="")
                print()
            print("{: >8}".format("Summ"), end="")
            for j in range(self.N):
                print("{: >8.2f}".format(summ_row[j]), end="")
            print("{: >8.2f}".format(sum(summ_column)), end="")
            print("{: >8.2f}".format(sum(normalized_column)), end="")
            print()
            print(f'Consistency ratio: {round((sum(summ_row * normalized_column) - N) / (0.9 * (N - 1)), 2)}')
            print("\n")

            if k != len(tables) - 1:
                alternative_comparing = np.vstack([alternative_comparing, normalized_column])
            else:
                criteria_comparing = np.array(normalized_column)
        print(alternative_comparing)
        print(np.dot(alternative_comparing[1:].T, criteria_comparing))


mc = MultiCriteria()
print("\nMETHOD OF CHANGES OF CRITERIA BY LIMITATION\n")
mc.criteria_to_limitation(1)
print("\nMETHOD OF PARETO SPACE NARROWING\n")
mc.pareto(1, 3)
print("\nMETHOD OF WEIGHING AND UNIFICATION\n")
mc.weighing_and_comparing()
print("\nMETHOD OF HIERARCHY ANALYSIS\n")
mc.hierarchy()
