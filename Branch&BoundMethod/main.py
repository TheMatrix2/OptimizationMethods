import numpy as np
from Simplex import Simplex


class BranchAndBound:
    def __init__(self, a, b, c, maximize=True):
        self.BaseA = a
        self.BaseB = b
        self.A = a
        self.B = b
        self.C = c
        self.Maximize=True
        self.OptimalSolution = np.zeros(len(c))

    def get_float(self, solution):
        for i in range(len(solution)):
            if solution[i] % 1 != 0:
                return i
        return -1

    def calculate(self):
        while
        simp = Simplex(self.A, self.B, self.C)
        simp.calculate()



C = np.array([2, 6, 7])
A = np.array([[3, 1, 1],
              [1, 2, 0],
              [0, 0.5, 2]])
B = np.array([3, 8, 1])

bandb = BranchAndBound(A, B, C)
bandb.calculate(A, B, C)
