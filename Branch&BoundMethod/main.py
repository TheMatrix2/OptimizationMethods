from BranchAndBound import *
from BruteForce import *

if __name__ == '__main__':
    C = np.array([2, 6, 7])
    A = np.array([[3, 1, 1],
                  [1, 2, 0],
                  [0, 0.5, 2]])
    B = np.array([3, 8, 1])

    bb1 = BranchAndBound(A, B, C)
    bb1.calculate(A, B)
    #
    # bb2 = BranchAndBound(A.T, C.T, B.T)
    # bb2.calculate(A.T, C.T)

    bf = BruteForce(A, B, C)
    bf.calculate()
