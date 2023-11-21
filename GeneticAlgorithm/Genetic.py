import random
import numpy as np
import math

P_CROSSOVER = 0.9
P_MUTATION = 0.25
MAX_GENERATIONS = 10

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def fitness_function(x, y):
    return math.cos(x)*math.cos(y)


class Genetic:
    def __init__(self, number_of_individuals, number_of_chromosomes):
        self.Population = np.zeros(number_of_individuals, number_of_chromosomes)

