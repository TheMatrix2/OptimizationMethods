class BruteForce:
    def __init__(self, a, b, c, minimize=True):
        self.A = a
        self.B = b
        self.C = c
        self.Minimize = minimize

    def calculate(self):
        maximum = max(self.B)
        if self.Minimize:
            min_value = 100
            for i in range(maximum, 0, -1):
                for j in range(maximum, 0, -1):
                    for k in range(maximum, 0, -1):
                        if self.A[0, 0] * i + self.A[0, 1] * j + self.A[0, 2] * k >= self.B[0] and \
                                self.A[1, 0] * i + self.A[1, 1] * j + self.A[1, 2] * k >= self.B[1] and \
                                self.A[2, 0] * i + self.A[2, 1] * j + self.A[2, 2] * k >= self.B[2]:
                            value = self.C[0] * i + self.C[1] * j + self.C[2] * k
                            if value < min_value:
                                min_value = value
                                print(f'Solution: [{i}, {j}, {k}]; Value: {value};')
            print(f'\nMinimal value of target function is {min_value}\n')

        else:
            max_value = 0
            for i in range(maximum):
                for j in range(maximum):
                    for k in range(maximum):
                        if self.A[0, 0] * i + self.A[0, 1] * j + self.A[0, 2] * k <= self.B[0] and \
                                self.A[1, 0] * i + self.A[1, 1] * j + self.A[1, 2] * k <= self.B[1] and \
                                self.A[2, 0] * i + self.A[2, 1] * j + self.A[2, 2] * k <= self.B[2]:
                            value = self.C[0] * i + self.C[1] * j + self.C[2] * k
                            print(f'Solution: [{i}, {j}, {k}]; Value: {value};')
                            if value > max_value:
                                max_value = value
            print(f'\nMaximal value of target function is {max_value}\n')
