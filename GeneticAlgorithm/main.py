import random


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

