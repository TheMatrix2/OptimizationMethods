import numpy as np

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DURATION = {'a': 3, 'b': 5, 'c': 2, 'd': 4, 'e': 3, 'f': 1, 'g': 4, 'h': 3, 'i': 3, 'j': 2, 'k': 5}
DEPENDENCIES = [[], ['a'], ['a'], ['a'], ['b'], ['c'], ['e', 'f'], ['c'], ['d'], ['h', 'i'], ['j', 'g'], ['k']]
EVENTS = [[], [0], [1], [1], [1], [2, 3], [3, 4], [5, 6], [7]]  # связь событий
# соответствие двух событий работам (по алфавиту от 0(a) до 9(k))
WORK_NAMES = [[0, 1], [1, 2], [1, 3], [1, 4], [2, 5], [3, 5], [5, 7], [3, 6], [4, 6], [6, 7], [7, 8]]


# топологическая сортировка
def topological_sort(dependencies, stack, index):
    for i in range(index, len(dependencies)):
        for j in range(i, len(dependencies)):
            if len(dependencies[i]) == 0 and i in dependencies[j]:
                if i not in stack:
                    stack.append(i)
                dependencies[j].remove(i)
                topological_sort(dependencies, stack, j)
    return stack


# поиск критического пути
def find_critical(dependencies, stack, index):
    for i in range(index, len(dependencies)):
        if len(stack) > 0 and stack[-1] > i:
            continue
        for j in range(i, len(dependencies)):
            if i in dependencies[j]:
                if i not in stack:
                    stack.append(i)
                find_critical(dependencies, stack, j)
    return stack


# вычисление раннего срока завершения каждого события
def earlier_terms(params_ev):
    for i in range(1, len(EVENTS)):
        params_ev[i, 0] = max([params_ev[EVENTS[i][j], 0] + DURATION[ALPHABET[WORK_NAMES.index([EVENTS[i][j], i])]]
                               for j in range(len(EVENTS[i]))])
    return params_ev


# вычисление позднего срока совершения каждого события
def later_terms(params_ev):
    params_ev[params_ev.shape[0] - 1, 1] = params_ev[params_ev.shape[0] - 1, 0]
    for i in range(len(EVENTS) - 2, 0, -1):
        next_works = []
        for j in range(len(EVENTS)):
            if i in EVENTS[j]:
                next_works.append(j)
        params_ev[i, 1] = min([params_ev[j, 1] - DURATION[ALPHABET[WORK_NAMES.index([i, j])]] for j in next_works])
    return params_ev


# вычисление параметров работ
def terms_works(params_ev, params_w):
    for i in range(len(params_w)):
        params_w[i, 0] = WORK_NAMES[i][0]   # начальное событие
        params_w[i, 1] = WORK_NAMES[i][1]   # конечное событие
        params_w[i, 2] = (params_ev[WORK_NAMES[i][0], 0] +  # ранний срок окончания
                          DURATION[ALPHABET[WORK_NAMES.index([WORK_NAMES[i][0], WORK_NAMES[i][1]])]])
        params_w[i, 3] = (params_ev[WORK_NAMES[i][1], 1] -  # поздний срок начала
                          DURATION[ALPHABET[WORK_NAMES.index([WORK_NAMES[i][0], WORK_NAMES[i][1]])]])
        params_w[i, 4] = (params_ev[WORK_NAMES[i][1], 1] - params_ev[WORK_NAMES[i][0], 0] -
                          DURATION[ALPHABET[WORK_NAMES.index([WORK_NAMES[i][0], WORK_NAMES[i][1]])]])   # полный резерв
        params_w[i, 5] = (params_ev[WORK_NAMES[i][1], 0] - params_ev[WORK_NAMES[i][0], 0] -
                          DURATION[ALPHABET[WORK_NAMES.index([WORK_NAMES[i][0], WORK_NAMES[i][1]])]])   # свободный
    return params_w


if __name__ == '__main__':
    w = []
    w = topological_sort(EVENTS, w, 0)
    w.append(len(EVENTS) - 1)
    print(f'Sorted: {w}')
    EVENTS = [[], [0], [1], [1], [1], [2, 3], [3, 4], [5, 6], [7]]
    events = earlier_terms(np.zeros((len(EVENTS), 3)))
    events = later_terms(events)
    for i in range(events.shape[0]):
        events[i, 2] = events[i, 1] - events[i, 0]
    works = terms_works(events, np.zeros((len(WORK_NAMES), 6)))

    print('\nEvents characteristics:')
    header = ['Event', 'Earliest start', 'Latest finish', 'Reserve']
    for col_name in header:
        print("{: >15}".format(col_name), end="")
    print()
    for i in range(events.shape[0]):
        print("{: >15}".format(i), end="")
        for j in range(events.shape[1]):
            print("{: >15}".format(int(events[i, j])), end="")
        print()

    print('\nWorks characteristics:')
    header = ['Name', 'Way', 'Duration', 'Earliest finish', 'Latest start', 'Total reserve', 'Free reserve']
    for col_name in header:
        print("{: >16}".format(col_name), end="")
    print()
    for i in range(works.shape[0]):
        print("{: >16}".format(ALPHABET[i]), end="")
        print("{: >16}".format(f'{int(works[i, 0])}->{int(works[i, 1])}'), end="")
        print("{: >16}".format(DURATION[ALPHABET[i]]), end="")
        for j in range(2, works.shape[1]):
            print("{: >16}".format(int(works[i, j])), end="")
        print()

    s = []
    s = find_critical(EVENTS, s, 0)
    s.append(len(EVENTS) - 1)
    print('\nCritical path:')
    for i in range(len(s)):
        if i != len(s) - 1:
            print(f'{s[i]}->', end="")
        else:
            print(f'{s[i]} = ', end="")
    length = 0
    for i in range(len(s) - 1):
        if i != len(s) - 2:
            print(f'{DURATION[ALPHABET[WORK_NAMES.index([s[i], s[i+1]])]]} + ', end="")
            length += DURATION[ALPHABET[WORK_NAMES.index([s[i], s[i+1]])]]
        else:
            print(f'{DURATION[ALPHABET[WORK_NAMES.index([s[i], s[i+1]])]]} = ', end="")
            length += DURATION[ALPHABET[WORK_NAMES.index([s[i], s[i+1]])]]
    print(length)

