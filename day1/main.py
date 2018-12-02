import time
import itertools


def input_file():
    with open("input.txt") as file:
        for line in file:
            yield int(line)


def puzzle_one():
    frequency = 0
    for value in input_file():
        frequency += value
    return frequency


def puzzle_two():
    result = None
    frequencies = {0}
    current_frequency = 0
    count = 0
    while result is None:
        count += 1
        for value in input_file():
            current_frequency += value
            if current_frequency in frequencies:
                result = current_frequency
                break
            frequencies.add(current_frequency)
    print(f"Loop count {count}")
    return result


def ridiculous_solution():
    frequencies = {0}
    current_frequency = 0
    for value in itertools.cycle(input_file()):
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
    count = 0
    while this_loop:
        count += 1
        with open("cameron.txt") as number_file:
            for line in number_file:
                total += int(line)
                if total in number_list:
                    this_loop = False
                    break
                number_list.add(total)
    print(f"Cameron loop count: {count}")
    return total  # This is probably wrong, as well.


before = time.monotonic()
print(puzzle_one())
print(puzzle_two())
print(cameron_two())
print(ridiculous_solution())
print(f"Total run time: {time.monotonic() - before}")