import numpy as np
from Simplex import Simplex

class BranchAndBound:
    def __init__(self, a, b, c, maximize=True):
        self.A = a
        self.B = b
        self.C = c

    def get_float(self, solution):
        for i in range(len(solution)):
            if solution[i] % 1 != 0:
                return i
        return -1


F = np.array([12, -1])
A = np.array([[6, -1],
              [2, 5]])
b = np.array([12, 20])

