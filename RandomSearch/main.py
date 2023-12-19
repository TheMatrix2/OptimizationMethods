import numpy as np
import matplotlib.pyplot as plt


def func_graph():
    x = np.arange(-3.5, 3.5, 0.01)
    func = (1 - x)**2 + np.exp(x)
    plt.plot(x, func)
    plt.plot(x, func * np.sin(5*x))
    plt.plot()
    plt.grid('True')
    plt.show()


if __name__ == '__main__':
    func_graph()
