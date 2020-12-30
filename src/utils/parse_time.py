"""
Module: Parse time

Public Functions:
    parse_time
"""


def parse_time(time: float) -> str:
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
    time_str = (
        f"{days} {_simple_plural(days, 'day')} "
        f"{hours} {_simple_plural(hours, 'hour')} "
        f"{minutes} {_simple_plural(minutes, 'minute')} "
        f"{seconds} {_simple_plural(seconds, 'second')} "
        f"{ms} {_simple_plural(ms, 'millisecond')}"
    )
    return time_str


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
