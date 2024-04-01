import numpy as np
import matplotlib.pyplot as plt
from math import exp, sin, log
from random import uniform


def unimodal_function(x):
    return (1 - x)**2 + exp(x)


def multimodal_function(x):
    return unimodal_function(x) * sin(5 * x)


def generate_value(func):
    x = uniform(-3.5, 3.5)
    f = func(x)
    return f


def func_graph():
    x = np.arange(-3.5, 3.5, 0.01)
    y = np.arange(-40, 40, 0.01)
    func = (1 - x)**2 + np.exp(x)
    plt.plot(x, func)
    plt.arrow(-3.5, 0, 7, 0, head_width=1, head_length=0.1, color='black')
    plt.arrow(0, -40, 0, 80, head_width=0.06, head_length=2, color='black')
    plt.plot(x, func * np.sin(5*x))
    plt.xlim(-3.5, 3.6)
    plt.ylim(-40, 42)
    plt.grid('True')
    plt.show()


def func_search(func, q, p):
    n = int((log(1 - p)/log(1 - q)) // 1 + 1)
    min_f = generate_value(func)
    for i in range(n):
        f = generate_value(func)
        if f < min_f:
            min_f = f
    return n, min_f


def print_info(table, integer=True):
    p = np.array([0.01 * p for p in range(90, 100, 1)])
    q = np.array([0.001 * q for q in range(5, 105, 5)])
    print("{: >8}".format("q\\p"), end="")
    for col_name in p:
        print("{: >8.2f}".format(col_name), end="")
    print()
    for i in range(table.shape[0]):
        print("{: >8.3f}".format(q[i]), end="")
        for j in range(table.shape[1]):
            if integer:
                print("{: >8}".format(round(table[i, j])), end="")
            else:
                print("{: >8.3f}".format(round(table[i, j], 3)), end="")
        print()


if __name__ == '__main__':
    func_graph()
    probabilities = np.array([0.01*p for p in range(90, 100, 1)])
    lengths = np.array([0.001*l for l in range(5, 105, 5)])
    table_n = np.zeros((lengths.shape[0], probabilities.shape[0]))
    table_min = np.zeros((lengths.shape[0], probabilities.shape[0]))
    for func in [unimodal_function, multimodal_function]:
        for i in range(len(lengths)):
            for j in range(len(probabilities)):
                n, min_f = func_search(func, lengths[i], probabilities[j])
                table_n[i, j], table_min[i, j] = round(n), round(min_f, 3)

        print_info(table_n)
        print()
        print_info(table_min, integer=False)
        print('\n\n')
