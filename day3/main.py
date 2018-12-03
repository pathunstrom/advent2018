from itertools import product
from itertools import tee
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
    claim_1: Claim
    claim_2: Claim
    disqualified = set()
    candidates = set()
    for claim_1, claim_2 in product(*tee(parse("input.txt", transform))):
        if claim_1.id == claim_2.id or (claim_1 in disqualified and claim_2 in disqualified):
            continue
        claim_1_set = set(claimed_inches(claim_1.dimensions))
        claim_2_set = set(claimed_inches(claim_2.dimensions))
        if claim_1_set.intersection(claim_2_set):
            # intersection means both are disqualified.
            candidates.discard(claim_1)
            candidates.discard(claim_2)
            disqualified.update({claim_1, claim_2})
        else:
            candidates.update({claim_1, claim_2})
    if len(candidates) == 1:
        return candidates.pop()
    else:
        raise WTFError(f"Candidates has {len(candidates)} members")


print(puzzle_one())  # 100261
print(puzzle_two())