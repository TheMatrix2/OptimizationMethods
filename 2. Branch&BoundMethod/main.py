from BranchAndBound import *
from BruteForce import *

if __name__ == '__main__':
    C = np.array([2, 6, 7])
    A = np.array([[3, 1, 1],
                  [1, 2, 0],
                  [0, 0.5, 2]])
    B = np.array([3, 8, 1])

    bb = BranchAndBound(A, B, C, minimize=False)
    bb.calculate(A, B)
    print(f'\nMinimal: {min(bb.Values)}') if bb.Minimize else print(f'Maximal: {max(bb.Values)}\n')

    bf = BruteForce(A, B, C, minimize=False)
    bf.calculate()
