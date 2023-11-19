import numpy as np
from Simplex import Simplex


# входные данные
c = np.array([2, 6, 7])
A = np.array([[3, 1, 1],
              [1, 2, 0],
              [0, 0.5, 2]])
b = np.array([3, 8, 1])

# для прямой задачи
print('\nDIRECT PROBLEM\n')
simplex_direct = Simplex(A, b, c)
simplex_direct.calculate()

# для двойственной задачи
print('\nDUAL PROBLEM\n')
simplex_dual = Simplex(A.T, c.T, b.T, maximize=False)
simplex_dual.calculate()
