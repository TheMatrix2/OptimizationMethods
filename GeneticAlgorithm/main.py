import random


def random_change(num, probability=0.25):
    s = list(num)
    for i in range(len(s)):
        if s[i] == '.':
            continue
        if random.random() < probability:
            s[i] = '0' if s[i] == '1' else '1'
    new_num = ""
    for e in s:
        new_num += e
    return new_num


s = random.uniform(-2, 2)
print(s)
b = float_to_binary(s)
print(b)
print(float(binary_to_float(b)))
new_b = random_change(b)
print(new_b)
print(binary_to_float(new_b))

