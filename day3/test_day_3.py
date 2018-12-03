import pytest

import day3.main as main


@pytest.mark.parametrize("test_input, expected", [
    ("#1 @ 906,735: 28x17\n", (1, (906, 735, 28, 17))),
    ("#2 @ 890,926: 12x29\n", (2, (890, 926, 12, 29))),
    ("#382 @ 23,690: 24x19\n", (382, (23, 690, 24, 19)))
])
def test_transform(test_input, expected):
    output = main.transform(test_input)
    assert len(output) == 2
    assert output[0] > 0
    assert len(output[1]) == 4
    assert output == expected


def test_update_counter_with_claim():
    counter = main.Counter()
    test_input = (3, 2, 5, 4)
    # ...........
    # ...........
    # ...XXXXX...
    # ...XXXXX...
    # ...XXXXX...
    # ...XXXXX...
    # ...........
    # ...........
    # ...........
    main.update_counter_with_claim(counter, test_input)
    assert sum(counter.values()) == 20


def test_has_no_intersection():
    test_input = main.Claim(1, (3, 2, 5, 4))
    test_counts = [(3, 2), (3, 2), (3, 3), (3, 4)]
    counter = main.Counter(test_counts)
    assert not main.has_no_intersection(counter, test_input)
    test_counts = [(8, 8), (9, 9), (100, 100)]
    counter = main.Counter(test_counts)
    assert main.has_no_intersection(counter, test_input)

