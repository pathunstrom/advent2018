import datetime as dt
from datetime import datetime

import pytest as pt

import day4.main as main

sample_lines = [
    "[1518-03-28 00:04] Guard #2663 begins shift",
    "[1518-10-18 00:53] wakes up",
    "[1518-04-02 00:45] falls asleep",
    "[1518-09-12 00:36] falls asleep",
    "[1518-07-06 00:59] wakes up",
    "[1518-03-15 23:46] Guard #2909 begins shift",
]

transform_output = [
    main.LogEntry(datetime(1518, 3, 28, 0, 4), main.State.BEGIN, 2663),
    main.LogEntry(datetime(1518, 10, 18, 0, 53), main.State.AWAKE),
    main.LogEntry(datetime(1518, 4, 2, 0, 45), main.State.ASLEEP),
    main.LogEntry(datetime(1518, 9, 12, 0, 36), main.State.ASLEEP),
    main.LogEntry(datetime(1518, 7, 6, 0, 59), main.State.AWAKE),
    main.LogEntry(datetime(1518, 3, 15, 23, 46), main.State.BEGIN, 2909)
]

sorted_output = [
    main.LogEntry(datetime(1518, 3, 15, 23, 46), main.State.BEGIN, 2909),
    main.LogEntry(datetime(1518, 3, 28, 0, 4), main.State.BEGIN, 2663),
    main.LogEntry(datetime(1518, 4, 2, 0, 45), main.State.ASLEEP),
    main.LogEntry(datetime(1518, 7, 6, 0, 59), main.State.AWAKE),
    main.LogEntry(datetime(1518, 9, 12, 0, 36), main.State.ASLEEP),
    main.LogEntry(datetime(1518, 10, 18, 0, 53), main.State.AWAKE),
]


@pt.mark.parametrize("test_value, expected_result", zip(sample_lines, transform_output))
def test_transform(test_value, expected_result):
    assert main.transform(test_value) == expected_result


def test_guard_id_regex():
    test_value = "Not me #5467 Not me"
    assert main.GUARD_ID.search(test_value).group(1) == "5467"

    test_value = "Not me #5t6"
    assert not main.GUARD_ID.search(test_value)


def test_guard_record():
    g = main.GuardRecord(1)
    now = datetime.now()
    g.add(main.LogEntry(now, main.State.BEGIN, 1))
    g.add(main.LogEntry(now + dt.timedelta(minutes=1), main.State.ASLEEP))
    g.add(main.LogEntry(now + dt.timedelta(minutes=11), main.State.AWAKE))

    assert g.sleep_time == 10

def test_sort_logs():
    assert main.sorted_logs(transform_output) == sorted_output


def test_processor():
    expected = {
        2909: main.GuardRecord(2909, logs=[
            main.LogEntry(datetime(1518, 3, 15, 23, 46), main.State.BEGIN, 2909)
        ]),
        2663: main.GuardRecord(2663, logs=[
            main.LogEntry(datetime(1518, 3, 28, 0, 4), main.State.BEGIN, 2663),
            main.LogEntry(datetime(1518, 4, 2, 0, 45), main.State.ASLEEP),
            main.LogEntry(datetime(1518, 7, 6, 0, 59), main.State.AWAKE),
            main.LogEntry(datetime(1518, 9, 12, 0, 36), main.State.ASLEEP),
            main.LogEntry(datetime(1518, 10, 18, 0, 53), main.State.AWAKE),
        ])
    }

    assert main.log_processor(sorted_output) == expected
