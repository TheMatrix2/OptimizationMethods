import numpy as np

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DURATION = {'a': 3, 'b': 5, 'c': 2, 'd': 4, 'e': 3, 'f': 1, 'g': 4, 'h': 3, 'i': 3, 'j': 2, 'k': 5}
DEPENDENCIES = [[], ['a'], ['a'], ['a'], ['b'], ['c'], ['e', 'f'], ['c'], ['d'], ['h', 'i'], ['j', 'g']]
s = []
p = np.zeros((len(DEPENDENCIES), 3))


def topological_sort(dependencies, stack, index):
    for i in range(index, len(dependencies) - 1):
        if len(dependencies[i]) == 0:
            for j in range(i, len(dependencies)):
                if ALPHABET[i] in dependencies[j]:
                    if ALPHABET[i] not in stack:
                        stack.append(ALPHABET[i])
                    dependencies[j].remove(ALPHABET[i])
                    topological_sort(dependencies, stack, j)
    return stack


def earlier_terms(params):
    for i in range(1, len(DEPENDENCIES)):
        if len(DEPENDENCIES[i]) == 1:
            params[i, 0] = params[ALPHABET.index(DEPENDENCIES[i][0]), 0] + DURATION[DEPENDENCIES[i][0]]
        else:
            params[i, 0] = max([params[ALPHABET.index(DEPENDENCIES[i][j]), 0] +
                                DURATION[DEPENDENCIES[i][j]] for j in range(len(DEPENDENCIES[i]))])
    return params


def later_terms(params):
    params[params.shape[0] - 1, 1] = params[params.shape[0] - 1, 0]
    for i in range(len(DEPENDENCIES) - 2, 0, -1):
        next_works = []
        for j in range(len(DEPENDENCIES)):
            if ALPHABET[i] in DEPENDENCIES[j]:
                next_works.append(ALPHABET[j])
        if len(next_works) == 1:
            params[i, 1] = params[ALPHABET.index(next_works[0]), 1] - DURATION[ALPHABET[i]]
        else:
            params[i, 1] = min([params[ALPHABET.index(next_works[j]), 1] -
                               DURATION[ALPHABET[j]] for j in range(len(next_works))])
    return params


s = topological_sort(DEPENDENCIES, s, 0)
s.append(ALPHABET[len(DEPENDENCIES) - 1])
print('Topologically sorted:')
print(s)
DEPENDENCIES = [[], ['a'], ['a'], ['a'], ['b'], ['c'], ['e', 'f'], ['c'], ['d'], ['h', 'i'], ['j', 'g']]
p = earlier_terms(p)
p = later_terms(p)
for i in range(p.shape[0]):
    p[i, 2] = p[i, 1] - p[i, 0]
print('\nEvents characteristics:')
print(p)
print('\nCritical way: ', end="")
for i in range(p.shape[0]):
    if p[i, 2] == 0:
        if i != p.shape[0] - 1:
            print(f'{ALPHABET[i]} - ', end="")
        else:
            print(ALPHABET[i], end="")
