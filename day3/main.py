from itertools import product
from itertools import chain
from collections import Counter
from collections import namedtuple

from acparse import parse

Claim = namedtuple("Claim", ["id", "dimensions"])

class WTFError(Exception): pass


def transform(line):
    values = line.split()
    identifier = int(values[0][1:])
    left, top = (int(v) for v in values[2].strip(":").split(","))
    width, height = (int(v) for v in values[3].split("x"))
    return Claim(identifier, (left, top, width, height))


def update_counter_with_claim(counter, claim):
    counter.update(claimed_inches(claim))
    return counter


def claimed_inches(claim):
    left, top, width, height = claim
    width_values = range(left, left + width)
    height_values = range(top, top + height)
    return product(width_values, height_values)


def has_no_intersection(counter, claim):
    counter.subtract(claimed_inches(claim.dimensions))
    for inch in claimed_inches(claim.dimensions):
        if counter[inch] >= 1:
            counter.update(claimed_inches(claim.dimensions))
            return False
    return True


def puzzle_one():
    """
    Right answer: 100261
    Wrong answers:
        * 116888
    """
    counts = Counter()
    for _, claim in parse("input.txt", transform):
        update_counter_with_claim(counts, claim)
    return sum(1 for _, v in counts.items() if v > 1)


def puzzle_two():
    """
    Right answer: 251
    """
    claims = list(parse("input.txt", transform))
    counter = Counter(chain(*(claimed_inches(claim.dimensions) for claim in claims)))
    for claim in claims:
        if has_no_intersection(counter, claim):
            return claim.id


print(puzzle_one())  # 100261
print(puzzle_two())