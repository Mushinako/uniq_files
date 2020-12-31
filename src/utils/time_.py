"""
Module: Parse time

Public Classes:
    Progress
    CalculationTime
    TimeTaken
"""

from dataclasses import dataclass
from time import time

from .print_funcs import progress_percent, progress_str


@dataclass
class Progress:
    """
    Progress recording
    """

    total: int
    current: int = 0

    def __str__(self) -> str:
        return self.string

    @property
    def string(self) -> str:
        return progress_str(self.current, self.total)

    @property
    def percentage(self) -> str:
        return progress_percent(self.current, self.total)


@dataclass
class CalculationTime:
    """
    Calculation time recording
    """

    left: int
    processed: int = 0
    time_taken: float = 0.0

    def __str__(self) -> str:
        return _time_str_short(self.time_taken)

    @property
    def time_left(self) -> str:
        return _time_remaining(self.left, self.processed, self.time_taken)


@dataclass
class TimeTaken:
    """
    Total time running taken
    """

    start: float = time()

    def __str__(self) -> str:
        return self.string

    @property
    def string(self) -> str:
        return _time_str(time() - self.start)


def _time_str(time: float) -> str:
    """
    Parse time in seconds into human-readable string

    Args:
        time (float): Time in seconds

    Returns:
        (str): Time string
    """
    ms = round(time * 1_000)
    seconds, ms = divmod(ms, 1_000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (
        f"{days} {_simple_plural(days, 'day')} "
        f"{hours} {_simple_plural(hours, 'hour')} "
        f"{minutes} {_simple_plural(minutes, 'minute')} "
        f"{seconds} {_simple_plural(seconds, 'second')} "
        f"{ms} {_simple_plural(ms, 'millisecond')}"
    )


def _time_str_short(time: float) -> str:
    """
    Parse time in seconds into human-readable string, short version

    Args:
        time (float): Time in seconds

    Returns:
        (str): Time string
    """
    seconds = round(time)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02}h {minutes:02}m {seconds:02}s"
    elif minutes:
        return f"{minutes:02}m {seconds:02}s"
    else:
        return f"{seconds:02}s"


def _time_remaining(left: int, processed: int, time_taken: float) -> str:
    """
    Calculate time remaining

    Args:
        left       (int): Amount of work left
        processed  (int): Amount of work processed
        time_taken (float): Time taken so far

    Returns:
        (str): Remaining time string
    """
    processed = processed or 1
    time_left = time_taken / processed * left
    return _time_str_short(time_left)


def _simple_plural(n: int, word: str) -> str:
    """
    Add `s` to words depending on plurality

    Args:
        n    (int): The number to be checked for plurality
        word (str): The word to be potentially pluralized

    Returns:
        (str): Completed string
    """
    return word if n == 1 else word + "s"
