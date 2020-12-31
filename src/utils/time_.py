"""
Module: Parse time

Public Functions:
    time_str
    time_str_short
    time_remaining
"""

from dataclasses import dataclass


@dataclass
class CalculationTime:
    """
    Calculation time recording
    """

    size_left: int
    size_processed: int = 0
    time_taken: float = 0.0


def time_str(time: float) -> str:
    """
    Parse time in seconds into human-readable string

    Args:
        time {float}: Time in seconds

    Returns:
        {str}: Time string
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


def time_str_short(time: float) -> str:
    """
    Parse time in seconds into human-readable string, short version

    Args:
        time {float}: Time in seconds

    Returns:
        {str}: Time string
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


def time_remaining(calculation_time: CalculationTime) -> str:
    """
    Calculate time remaining

    Args:
        calculation_time {CalculationTime}: Data for processed calculation time

    Returns:
        {str}: Remaining time string
    """
    size_processed = calculation_time.size_processed or 1
    time_left = (
        calculation_time.time_taken / size_processed * calculation_time.size_left
    )
    return time_str_short(time_left)


def _simple_plural(n: int, word: str) -> str:
    """
    Add `s` to words depending on plurality

    Args:
        n    {int}: The number to be checked for plurality
        word {str}: The word to be potentially pluralized

    Returns:
        {str}: Completed string
    """
    return word if n == 1 else word + "s"
