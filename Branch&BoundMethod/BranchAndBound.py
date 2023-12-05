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
        self.Count = 0

    def find_float(self, solution):
        for i in range(len(solution)):
            if solution[i] != 0 and solution[i] % 1 != 0:
                return i
        return len(solution)

    def calculate(self, a, b):
        simp = Simplex(a, b, self.C, self.Minimize)
        simp.calculate()
        simp.print_info()
        if not simp.solution_exists():
            print('\nSOLUTION DOES NOT EXIST\n')
            return
        if len(self.Values) != 0 and ((self.Minimize and simp.find_func_value() > min(self.Values)) or
                                      (not self.Minimize and simp.find_func_value() < max(self.Values))):
            print(f'Value {simp.find_func_value()} '
                  f'{"is more than minimal" if self.Minimize else "is less than maximal"} {max(self.Values)}\n')
            return
        k = self.find_float(simp.Solution)
        try:
            if k == len(simp.Solution):
                if len(self.Values) == 0 or (self.Minimize and simp.find_func_value() < min(self.Values)) or \
                        (not self.Minimize and simp.find_func_value() > max(self.Values)):
                    self.Values.append(simp.find_func_value())
                    self.Solutions.append([simp.Solution])
                    print(f'Solutions: {self.Solutions}')
                    print(f'Values: {self.Values}')
                    print(f'Minimal: {min(self.Values)}') if self.Minimize else print(f'Maximal: {max(self.Values)}')
                    print(f'Nodes: {self.Nodes}\n')
                    return
        except:
            return

        self.Count += 1
        print(f'{self.Count} LEVEL\n')
        node = round(simp.Solution[k], 2)
        print(f'Branching by {node} on x <= {node // 1} and x >= {node // 1 + 1}')
        self.Nodes.append(f'x{k+1} = {node}\n')

        print(f'Add x{k+1} <= {node // 1}\n')
        new_lhs = np.zeros(self.A.shape[1])
        new_lhs[k] = 1 if not self.Minimize else -1
        self.calculate(a=np.vstack([self.A, new_lhs]), b=np.append(self.B, node//1 if not self.Minimize else -node//1))

        print(f'Add x{k + 1} >= {node // 1 + 1}\n')
        new_lhs = np.zeros(self.A.shape[1])
        new_lhs[k] = -1 if not self.Minimize else 1
        self.calculate(a=np.vstack([self.A, new_lhs]), b=np.append(self.B, -(node//1+1) if not self.Minimize else node//1+1))
