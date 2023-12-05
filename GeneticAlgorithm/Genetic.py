import random
import numpy as np
import math
import matplotlib.pyplot as plt

P_CROSSOVER = 0.9
P_MUTATION = 0.25
MAX_GENERATIONS = 10

RANDOM_SEED = 1
random.seed(RANDOM_SEED)


def fitness_function(ind):
    return math.cos(ind[0])*math.cos(ind[1])


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


def mutation(chromosome, probability=0.1):
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

    def create(self):
        for i in range(self.NumberOfIndividuals):
            gen1 = random.uniform(-2, 2)
            gen2 = random.uniform(-2, 2)
            self.Individuals[i][0], self.Individuals[i][1] = gen1, gen2
            self.Fitness[i] = fitness_function([gen1, gen2])
            # summ += self.Fitness[i]
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
                add = self.Individuals[k1]
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
            if random.random() < P_CROSSOVER:
                child1, child2 = crossover([float_to_binary(parents[i1][0]), float_to_binary(parents[i1][1])],
                                           [float_to_binary(parents[i2][0]), float_to_binary(parents[i2][1])])
            else:
                child1, child2 = ([float_to_binary(parents[i1][0]), float_to_binary(parents[i1][1])],
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


class Genetic:
    def __init__(self, number_of_individuals, number_of_chromosomes):
        self.Population = Population(number_of_individuals, number_of_chromosomes)
        self.Population.create()
        self.AllFitness = []
        self.AllMaxFitness = []
        self.Generation = 0
        self.Maximum = 0

    def print_info(self):
        print(f'Generation: {self.Generation}')
        print('Population: ')
        print(self.Population.Individuals)
        print(f'Average fitness: {self.Population.AverageFitness}')
        print(f'Maximal fitness: {self.Population.MaxFitness}')
        print(f'Maximum at all: {self.Maximum}\n')

    def calculate(self):
        generation = 0
        self.AllFitness.append(self.Population.AverageFitness)
        self.print_info()
        while self.Generation != MAX_GENERATIONS:
            self.Population.generate_new()
            self.AllFitness.append(self.Population.AverageFitness)
            self.AllMaxFitness.append(self.Population.MaxFitness)
            if self.Population.MaxFitness > self.Maximum:
                self.Maximum = self.Population.MaxFitness
            self.Generation += 1
            self.print_info()

    def get_diagram(self):
        plt.scatter(np.arange(0, len(self.AllFitness), 1), self.AllFitness, color='blue')
        plt.plot(self.AllMaxFitness, color='red')
        plt.show()
