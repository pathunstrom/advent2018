import re
from collections import Counter
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import List
from typing import NamedTuple

from acparse import parse

GUARD_ID = re.compile(r"#(\d+)\b")

class State(Enum):
    ASLEEP = "asleep"
    AWAKE = "wakes"
    BEGIN = "shift"


@dataclass
class GuardRecord:
    id: int
    logs: List['LogEntry'] = field(default_factory=list)

    def add(self, log_entry: 'LogEntry'):
        self.logs.append(log_entry)

    @property
    @lru_cache()
    def sleep_time(self):
        total = 0
        sleep_at = None
        for entry in self.logs:
            if entry.state is State.ASLEEP:
                assert isinstance(entry.time, datetime)
                sleep_at = entry.time
            elif entry.state is State.AWAKE:
                if sleep_at is None:
                    raise TypeError(f"Logs for Guard {self.id} are out of order.")
                total += (entry.time - sleep_at).seconds // 60
                sleep_at = None
        return total

    @property
    @lru_cache()
    def minutes(self) -> Counter:
        minutes = []
        sleep_at = None
        for entry in self.logs:
            if entry.state is State.ASLEEP:
                sleep_at = entry.time.minute
            elif entry.state is State.AWAKE:
                minutes.extend(list(range(sleep_at, entry.time.minute)))
                sleep_at = None
        return Counter(minutes)

    def __hash__(self):
        return super().__hash__()


class LogEntry(NamedTuple):
    time: datetime
    state: State
    id: int = None


def transform(value: str):
    entry_time, entry = value.split("]")
    entry_time = datetime.strptime(entry_time.strip("["), "%Y-%m-%d %H:%M")
    entry_id = None
    entry_state = None
    for state in State:
        if state.value in entry:
            entry_state = state
            if state is State.BEGIN:
                entry_id = int(GUARD_ID.search(entry).group(1))
    if entry_state is None:
        raise ValueError("Entry does not contain a valid reference.")
    return LogEntry(entry_time, entry_state, entry_id)


def sorted_logs(logs):
    return sorted(logs, key=lambda x: x[0])


def log_processor(presorted_logs: List[LogEntry]):
    guards = {}
    current_guard = None
    for entry in presorted_logs:
        if entry.id:
            try:
                current_guard = guards[entry.id]
            except KeyError:
                current_guard = GuardRecord(entry.id, [])
                guards[entry.id] = current_guard
        current_guard.add(entry)
    return guards


def process_guards():
    return log_processor(sorted_logs(parse("input.txt", transform)))


def puzzle_one():
    guards = process_guards()
    best_bet = sorted(guards.values(), key=lambda x: x.sleep_time)[-1]
    best_minute = best_bet.minutes.most_common(1)[0][0]
    return best_bet.id * best_minute


def puzzle_two():
    def highest_minute_count(guard: GuardRecord):
        try:
            return guard.minutes.most_common(1)[0][1]
        except IndexError:
            return 0

    best = list(sorted(process_guards().values(), key=highest_minute_count))[-1]
    return best.id * best.minutes.most_common(1)[0][0]


print(puzzle_one())
print(puzzle_two())
