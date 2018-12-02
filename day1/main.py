import time
import itertools

from acparse import parse

def puzzle_one():
    frequency = 0
    for value in parse("input.txt", int):
        frequency += value
    return frequency


def puzzle_two():
    result = None
    frequencies = {0}
    current_frequency = 0
    while result is None:
        for value in parse("input.txt", int):
            current_frequency += value
            if current_frequency in frequencies:
                result = current_frequency
                break
            frequencies.add(current_frequency)
    return result


def ridiculous_solution():
    frequencies = {0}
    current_frequency = 0
    for value in itertools.cycle(parse("input.txt", int)):
        current_frequency += value
        if current_frequency in frequencies:
            return current_frequency
        frequencies.add(current_frequency)


def cameron_two():
    # Then we indent the rest of the program to happen inside
    # the context.
    # Nothing else has changed.
    number_list = {0}  # this is right.
    total = 0
    this_loop = True  # This might have a better solution.
    while this_loop:
        with open("cameron.txt") as number_file:
            for line in number_file:
                total += int(line)
                if total in number_list:
                    this_loop = False
                    break
                number_list.add(total)
    return total  # This is probably wrong, as well.


print(f"Puzzle one: {puzzle_one()}")
print(f"Puzzle two: {puzzle_two()}")
print(f"Bro's solution: {cameron_two()}")
print(f"Better puzzle two: {ridiculous_solution()}")
