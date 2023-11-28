from Simplex import *


class BranchAndBound:
    def __init__(self, a, b, c, minimize=True):
        # self.BaseA = a
        # self.BaseB = b
        self.A = a
        self.B = b
        self.C = c
        self.Minimize = minimize
        self.Solutions = []
        self.Values = []
        self.Nodes = []

    def find_float(self, solution):
        for i in range(len(solution)):
            if solution[i] != 0 and solution[i] % 1 != 0:
                return i
        return False

    def calculate(self, a, b):
        simp = Simplex(a, b, self.C, self.Minimize)
        simp.calculate()
        i = k = self.find_float(simp.Solution)
        while True:
            flag1 = flag2 = False
            print('Solution is not integer')
            node = simp.Solution[i]
            self.Nodes.append(node)
            print(f'Branching by {node} on x <= {node // 1} and x >= {node // 1 + 1}')
            new_s = np.zeros(self.A.shape[1])
            new_s[i] = 1
            A = np.vstack([self.A, new_s])
            B = np.append(self.B, node // 1)
            simp_under = Simplex(A, B, self.C, self.Minimize)
            simp_under.calculate()
            if not simp_under.check():
                flag1 = True
            i = self.find_float(simp_under.Solution)
            if i == -1:
                s = 0
                for l in range(len(simp_under.Solution)):
                    s += simp_under.Function[l] * simp_under.Solution[l]
                print(f'Value of target function: {round(s, 2)}')
                print(f'Solution: {simp_under.Solution}')
                self.Values.append(s)
                self.Solutions.append(simp_under.Solution)
                flag1 = True


            node = simp.Solution[k]
            self.Nodes.append(node)
            print(f'Branching by {node} on x <= {node // 1} and x >= {node // 1 + 1}')
            new_s = np.zeros(self.A.shape[1])
            new_s[k] = -1
            A = np.vstack([self.A, new_s])
            B = np.append(self.B, -(node // 1 + 1))
            simp_above = Simplex(A, B, self.C, self.Minimize)
            simp_above.calculate()
            if not simp_above.check():
                flag2 = True
            k = self.find_float(simp_above.Solution)
            if k == -1:
                s = 0
                for j in range(len(simp_above.Solution)):
                    s += simp_above.Function[j] * simp_above.Solution[j]
                print(f'Value of target function: {round(s, 2)}')
                print(f'Solution: {simp_above.Solution}')
                self.Values.append(s)
                self.Solutions.append(simp_above.Solution)
                flag2 = True

            if flag1 and flag2:
                break


C = np.array([2, 6, 7])
A = np.array([[3, 1, 1],
              [1, 2, 0],
              [0, 0.5, 2]])
B = np.array([3, 8, 1])

bandb = BranchAndBound(A, B, C)
bandb.calculate(A, B)
