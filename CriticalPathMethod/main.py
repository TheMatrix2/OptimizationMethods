import numpy as np

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DURATION = {'a': 3, 'b': 5, 'c': 2, 'd': 4, 'e': 3, 'f': 1, 'g': 4, 'h': 3, 'i': 3, 'j': 2, 'k': 5}
DEPENDENCIES = [[], ['a'], ['a'], ['a'], ['b'], ['c'], ['e', 'f'], ['c'], ['d'], ['h', 'i'], ['j', 'g'], ['k']]
PROCESSES = sum([len(x) for x in DEPENDENCIES])
s = []
events = np.zeros((len(DEPENDENCIES), 3))
works = np.zeros((PROCESSES, 6))
works_names = []
for i in range(len(DEPENDENCIES)):
    for j in range(i, len(DEPENDENCIES)):
        if ALPHABET[i] in DEPENDENCIES[j]:
            works_names.append([i, j])


def topological_sort(dependencies, stack, index):
    for i in range(index, len(dependencies)):
        if len(dependencies[i]) == 0:
            for j in range(i, len(dependencies)):
                if ALPHABET[i] in dependencies[j]:
                    if i not in stack:
                        stack.append(i)
                    dependencies[j].remove(ALPHABET[i])
                    topological_sort(dependencies, stack, j)
    return stack


def earlier_terms(params_ev):
    for i in range(1, len(DEPENDENCIES)):
        if len(DEPENDENCIES[i]) == 1:
            params_ev[i, 0] = params_ev[ALPHABET.index(DEPENDENCIES[i][0]), 0] + DURATION[DEPENDENCIES[i][0]]
        else:
            params_ev[i, 0] = max([params_ev[ALPHABET.index(DEPENDENCIES[i][j]), 0] +
                                DURATION[DEPENDENCIES[i][j]] for j in range(len(DEPENDENCIES[i]))])
    params_ev[len(DEPENDENCIES)-1, 0] = (params_ev[ALPHABET.index(DEPENDENCIES[len(DEPENDENCIES)-1][0]), 0] +
                                         DURATION[DEPENDENCIES[len(DEPENDENCIES)-1][0]])
    return params_ev


def later_terms(params_ev):
    params_ev[params_ev.shape[0] - 1, 1] = params_ev[params_ev.shape[0] - 1, 0]
    for i in range(len(DEPENDENCIES) - 2, 0, -1):
        next_works = []
        for j in range(len(DEPENDENCIES)):
            if ALPHABET[i] in DEPENDENCIES[j]:
                next_works.append(ALPHABET[j])
        if len(next_works) == 1:
            params_ev[i, 1] = params_ev[ALPHABET.index(next_works[0]), 1] - DURATION[ALPHABET[i]]
        else:
            params_ev[i, 1] = min([params_ev[ALPHABET.index(next_works[j]), 1] -
                               DURATION[ALPHABET[j]] for j in range(len(next_works))])
    return params_ev


def terms_works(params_ev, params_w):
    for i in range(len(params_w)):
        params_w[i, 0] = works_names[i][0]
        params_w[i, 1] = works_names[i][1]
        params_w[i, 2] = params_ev[works_names[i][0], 0] + DURATION[ALPHABET[works_names[i][0]]]
        params_w[i, 3] = params_ev[works_names[i][1], 1] - DURATION[ALPHABET[works_names[i][0]]]
        params_w[i, 4] = (params_ev[works_names[i][1], 1] - params_ev[works_names[i][0], 0] -
                          DURATION[ALPHABET[works_names[i][0]]])
        params_w[i, 5] = (params_ev[works_names[i][1], 0] - params_ev[works_names[i][0], 0] -
                          DURATION[ALPHABET[works_names[i][0]]])
    return params_w


s = topological_sort(DEPENDENCIES, s, 0)
s.append(len(DEPENDENCIES)-1)
print('Topologically sorted:')
print(s)
DEPENDENCIES = [[], ['a'], ['a'], ['a'], ['b'], ['c'], ['e', 'f'], ['c'], ['d'], ['h', 'i'], ['j', 'g'], ['k']]
events = earlier_terms(events)
events = later_terms(events)
works = terms_works(events, works)
for i in range(events.shape[0]):
    events[i, 2] = events[i, 1] - events[i, 0]
print('\nEvents characteristics:')
print(events)
print('\nWorks characteristics:')
print(works)
print('\nCritical way: ', end="")
for i in range(events.shape[0]):
    if events[i, 2] == 0:
        if i != events.shape[0] - 1:
            print(f'{i} - ', end="")
        else:
            print(i, end="")
