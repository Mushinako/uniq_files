"""
Module: Calculation progress

Public Classes:
    Progress : Code run progress
    ETA      : ETA to code finish
    TotalTime: Total time taken by code
"""

from dataclasses import dataclass
from time import time

from progbar import progress_percent, progress_str


@dataclass
class Progress:
    """
    Code run progress

    Args:
        total   (int): Total number of elements
        current (int): ID of current element

    Public Attributes:
        total   (int)         : Total number of elements
        current (int)         : ID of current element
        string  (readonly str): String representation of progress
        percent (readonly str): Percent representation of progress
    """

    total: int
    current: int = 0

    @property
    def string(self) -> str:
        return progress_str(self.current, self.total)

    @property
    def percent(self) -> str:
        return progress_percent(self.current, self.total)


@dataclass
class ETA:
    """
    ETA to code finish

    Args:
        left       (int)  : Number of elements left
        processed  (int)  : ID of current element
        time_taken (float): Time taken for all processed elements

    Public Attributes:
        left       (int)         : Number of elements left
        processed  (int)         : ID of current element
        time_taken (float)       : Time taken for all processed elements
        string     (readonly str): String representation of ETA
    """

    left: int
    processed: int = 0
    time_taken: float = 0.0

    @property
    def string(self) -> str:
        return _time_remaining(self.left, self.processed, self.time_taken)


@dataclass
class TotalTime:
    """
    Total time taken by code

    Public Attributes:
        start  (float)       : Unix timestamp when code started
        string (readonly str): String representation of total time taken
    """

    start: float = time()

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
        left       (int)  : Number of elements left
        processed  (int)  : ID of current element
        time_taken (float): Time taken for all processed elements

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
