import random
import numpy as np
import math

P_CROSSOVER = 0.9
P_MUTATION = 0.25
MAX_GENERATIONS = 10

RANDOM_SEED = 42
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
    return '{0}.{1}'.format(integer_part, fractional_part)


def binary_to_float(binary_str):
    # sign = 1 if (binary_str[0] == '0' or binary_str[0] == '1') else -1
    parts = binary_str.split('.')

    integer_part = parts[0]

    fractional_part = 0.0
    if len(parts) == 2:
        for i in range(len(parts[1])):
            fractional_part += int(parts[1][i]) * 2**(-(i + 1))
    frac_part = str(fractional_part)

    return integer_part + frac_part[1:]


def crossover(child1, child2):
    pass


def mutation(ind, probability=P_MUTATION):
    pass


class Population:
    def __init__(self, number_of_individuals, number_of_chromosomes):
        self.NumberOfIndividuals = number_of_individuals
        self.NumberOfChromosomes = number_of_chromosomes
        self.Individuals = np.zeros(number_of_individuals, number_of_chromosomes)
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
        offspring = np.array([])
        for i in range(self.NumberOfIndividuals):
            k1 = k2 = 0
            while k1 == k2:
                k1, k2 = (random.randint(0, self.NumberOfIndividuals - 1),
                          random.randint(0, self.NumberOfIndividuals - 1))
            offspring = np.hstack([offspring, max(self.Individuals[k1], self.Individuals[k2], key=fitness_function)])

        return offspring

    def recalculate(self):
        pass


class Genetic:
    def __init__(self, number_of_individuals, number_of_chromosomes):
        self.Population = Population(number_of_individuals, number_of_chromosomes)
        self.AllFitness = []

