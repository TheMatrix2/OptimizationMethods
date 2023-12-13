import numpy as np

from Simplex import *

MATRIX = np.array([[6, 17, 16, 18, 15],
                   [18, 8, 16, 8, 8],
                   [6, 13, 18, 4, 3],
                   [15, 14, 2, 18, 19]])

print('PLAYER A\n')
B = np.ones(MATRIX.shape[1])
C = np.ones(MATRIX.shape[0])
simp = Simplex(MATRIX.T, B, C)
simp.calculate()
simp.print_info()
print(f'\nSolution: {[round(s, 3) for s in simp.Solution]}'
      f'\nFunction value: {round(simp.find_func_value(), 3)} -> minimal gain: {round(1/simp.find_func_value(), 3)}')
optimal_strategy = simp.Solution * round(1/simp.find_func_value(), 3)
print(f'\nOptimal mixed strategy for player A:')
for s in optimal_strategy:
    print(round(s, 3))

print('\n\nPLAYER B\n')
B = np.ones(MATRIX.shape[0])
C = np.ones(MATRIX.shape[1])
simp = Simplex(MATRIX, B, C, minimize=False)
simp.calculate()
simp.print_info()
print(f'\nSolution: {[round(s, 3) for s in simp.Solution]}'
      f'\nFunction value: {round(simp.find_func_value(), 3)} -> maximal gain: {round(1/simp.find_func_value(), 3)}')
optimal_strategy = simp.Solution * round(1/simp.find_func_value(), 3)
print(f'\nOptimal mixed strategy for player B:')
for s in optimal_strategy:
    print(round(s, 3))
