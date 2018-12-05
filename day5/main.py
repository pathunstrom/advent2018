import string
import time
from itertools import count

from acparse import parse


def strip_polymer(polymer, target):
    return ''.join(c for c in polymer if c not in target)


def reduce_polymer(polymer):
    output = []
    for index, unit in enumerate(polymer):
        output.append(unit)
        other = output[index - 1]
        if other and unit.lower() == other.lower() and unit != other:
            output[index - 1] = None
            output[index] = None
    return ''.join(u for u in output if u is not None)


def reduce_polymer_to_minimum(polymer):
    for c in count(1):
        output = reduce_polymer(polymer)
        if polymer == output:
            return output
        polymer = output


assert reduce_polymer('aA') == ''
assert reduce_polymer('abBA') == 'aA'
assert reduce_polymer('abAB') == 'abAB'
assert reduce_polymer('aabAAB') == 'aabAAB'
assert reduce_polymer_to_minimum('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'

def puzzle_one():
    for line in parse("input.txt"):
        return reduce_polymer_to_minimum(line)


def puzzle_two():
    polymer = list(parse("input.txt"))[0]
    optimal_score = None
    for target in zip(string.ascii_uppercase, string.ascii_lowercase):
        score = len(reduce_polymer_to_minimum(strip_polymer(polymer, target)))
        if optimal_score is None:
            optimal_score = score
        elif score < optimal_score:
            optimal_score = score
    return optimal_score

start = time.time()
print(len(puzzle_one()))
print(f"Puzzle one solved in {time.time() - start} seconds")
start = time.time()
print(puzzle_two())
print(f"Puzzle two solved in {time.time() - start}")