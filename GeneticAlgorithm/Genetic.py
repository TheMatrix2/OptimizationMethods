import random
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

P_MUTATION = 0.3
MAX_GENERATIONS = 10

def fitness_function(ind):
    return math.cos(ind[0])*math.cos(ind[1])


def fitness_function_graphic():
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    x = np.arange(-2, 2, 0.01)
    y = np.arange(-2, 2, 0.01)
    x, y = np.meshgrid(x, y)
    z = np.cos(x)*np.cos(y)
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def float_to_binary(num):
    exponent = 0
    shifted_num = num
    while shifted_num != int(shifted_num):
        shifted_num *= 2
        exponent += 1
    if exponent == 0:
        return '{0:0b}'.format(int(shifted_num))
    binary = '{0:0{1}b}'.format(int(shifted_num), exponent+1)
    integer_part = binary[:-exponent]
    fractional_part = binary[-exponent:].rstrip('0')
    return ('{0}.{1}'.format(integer_part, fractional_part))[:50 - 1]


def binary_to_float(binary_str):
    parts = binary_str.split('.')

    integer_part = parts[0]

    fractional_part = 0.0
    if len(parts) == 2:
        for i in range(len(parts[1])):
            fractional_part += int(parts[1][i]) * 2**(-(i + 1))
    frac_part = str(fractional_part)

    return integer_part + frac_part[1:]


def crossover(child1, child2):
    s1 = random.randint(3, len(child1[0]) - 3)
    s2 = random.randint(3, len(child1[1]) - 3)
    children = [[child1[0], child1[1]], [child2[0], child2[1]]]
    for i in range(len(children)):
        for j in range(len(children[i])):
            children[i][j] = list(children[i][j])
    children[0][0][:s1], children[1][0][:s1] = children[1][0][:s1], children[0][0][:s1]
    children[0][1][:s2], children[1][1][:s2] = children[1][1][:s2], children[0][1][:s2]
    result = [["", ""],
              ["", ""]]
    for i in range(len(children)):
        for j in range(len(children[i])):
            temp = ""
            for s in children[i][j]:
                temp += s
            result[i][j] = temp

    return [result[0][0], result[0][1]], [result[1][0], result[1][1]]


def mutation(chromosome, probability=0.04):
    s = list(chromosome)
    for i in range(len(s)):
        if s[i] == '.' or s[i] == '-':
            continue
        if random.random() < probability:
            s[i] = '0' if s[i] == '1' else '1'
    new_chromosome = ""
    for e in s:
        new_chromosome += e
    chromosome = new_chromosome

    return chromosome


class Population:
    def __init__(self, number_of_individuals, number_of_chromosomes):
        self.NumberOfIndividuals = number_of_individuals
        self.NumberOfChromosomes = number_of_chromosomes
        self.Individuals = np.zeros((number_of_individuals, number_of_chromosomes))
        self.Fitness = np.zeros(number_of_individuals)
        self.AverageFitness = 0
        self.MaxFitness = 0
        self.History = []

    def create(self):
        for i in range(self.NumberOfIndividuals):
            gen1 = random.uniform(-2, 2)
            gen2 = random.uniform(-2, 2)
            self.Individuals[i][0], self.Individuals[i][1] = gen1, gen2
            self.Fitness[i] = fitness_function([gen1, gen2])
        summ = np.sum(self.Fitness)
        self.AverageFitness = summ / self.NumberOfIndividuals
        self.MaxFitness = max(self.Fitness)

    def select_tournament(self):
        offspring = np.array([0, 0])
        for i in range(self.NumberOfIndividuals):
            k1 = k2 = 0
            while k1 == k2:
                k1, k2 = (random.randint(0, self.NumberOfIndividuals - 1),
                          random.randint(0, self.NumberOfIndividuals - 1))
            if fitness_function(self.Individuals[k1]) > fitness_function(self.Individuals[k2]):
                offspring = np.vstack([offspring, self.Individuals[k1]])
            else:
                offspring = np.vstack([offspring, self.Individuals[k2]])
        return offspring

    def generate_new(self):
        parents = self.select_tournament()[1:]
        children = []
        indexes = [x for x in range(len(self.Individuals))]
        random.shuffle(indexes)
        for i1, i2 in zip(indexes[::2], indexes[1::2]):
            child1, child2 = crossover([float_to_binary(parents[i1][0]), float_to_binary(parents[i1][1])],
                                       [float_to_binary(parents[i2][0]), float_to_binary(parents[i2][1])])
            children.append(child1)
            children.append(child2)

        for i in range(len(children)):
            if random.random() < P_MUTATION:
                children[i] = [mutation(children[i][0]), mutation(children[i][1])]
            self.Individuals[i] = [binary_to_float(children[i][0]), binary_to_float(children[i][1])]
        for i in range(self.NumberOfIndividuals):
            self.Fitness[i] = fitness_function(self.Individuals[i])
        summ = np.sum(self.Fitness)
        self.AverageFitness = summ / self.NumberOfIndividuals
        self.MaxFitness = max(self.Fitness)
        for i in range(self.NumberOfIndividuals):
            self.History.append(self.Individuals[i])


class Genetic:
    def __init__(self, number_of_individuals, number_of_chromosomes):
        self.Population = Population(number_of_individuals, number_of_chromosomes)
        self.Population.create()
        self.AllAverageFitness = []
        self.AllMaxFitness = []
        self.Generation = 0
        self.Maximum = 0
        self.x = []
        self.y = []

    def print_info(self):
        print(f'\nGeneration: {self.Generation}')
        print('Population: ')
        print("{: >5}".format(""), end="")
        print("{: >9}".format(f"chromo1"), end="")
        print("{: >9}".format(f"chromo2"), end="")
        print()
        for i in range(self.Population.NumberOfIndividuals):
            print("{: >5}".format(f"ind{i+1}"), end="")
            self.x.append(self.Population.Individuals[i, 0])
            self.y.append(self.Population.Individuals[i, 1])
            for j in range(self.Population.NumberOfChromosomes):
                print("{: >9.5f}".format(round(self.Population.Individuals[i, j], 5)), end="")
            print()
        print(f'\nAverage fitness: {round(self.Population.AverageFitness, 5)}')
        print(f'Maximal fitness: {round(self.Population.MaxFitness, 5)}')
        print(f'Maximum at all: {round(self.Maximum, 5)}\n')

    def calculate(self):
        self.AllAverageFitness.append(self.Population.AverageFitness)
        self.print_info()
        while self.Generation != MAX_GENERATIONS:
            self.Population.generate_new()
            self.AllAverageFitness.append(self.Population.AverageFitness)
            self.AllMaxFitness.append(self.Population.MaxFitness)
            if self.Population.MaxFitness > self.Maximum:
                self.Maximum = self.Population.MaxFitness
            self.Generation += 1
            self.print_info()

    def get_diagram(self):
        plt.scatter(np.arange(0, len(self.AllAverageFitness), 1), self.AllAverageFitness, color='blue')
        plt.xlabel('Поколения')
        plt.ylabel('Средняя приспособленность (max=1)')
        plt.grid(True)
        plt.show()

        colors = np.array([x*100/(MAX_GENERATIONS*4+4) for x in range(MAX_GENERATIONS*4+4)])
        plt.scatter(self.x, self.y, c=colors, cmap='viridis')
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.xlabel('Хромосома 1')
        plt.ylabel('Хромосома 2')
        plt.grid(True)
        plt.show()
