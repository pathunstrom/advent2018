from collections import Counter
from itertools import product

from acparse import parse

def puzzle_one():
    # Bad answer: 17199
    twos = 0
    threes = 0
    value: str
    for value in parse("input.txt"):
        counts = Counter(value.strip())
        values = set(counts.values())
        if 2 in values:
            twos += 1
        if 3 in values:
            threes += 1
    return twos * threes


def puzzle_two():
    values = [v for v in parse("input.txt", lambda x: x.strip())]
    for checksum1, checksum2 in product(values, values):
        number_of_differences = 0
        sames = []
        for letter_one, letter_two in zip(checksum1, checksum2):
            if letter_one == letter_two:
                sames.append(letter_one)
            else:
                number_of_differences += 1
        if number_of_differences == 1:
            return "".join(sames)


print(puzzle_one())  # 6642
print(puzzle_two())  # cvqlbidheyujgtrswxmckqnap
