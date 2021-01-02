"""
Module: `print`-related helper functions

Public Functions:
    clear_print          : Clear line and print
    clear_print_clearable: Clear line and print clearable
    progress_str         : Generate progress string
    progress_percent     : Generate progress percentage
    shrink_str           : Shrink string to fit on console
"""

from shutil import get_terminal_size
from typing import Any, Optional


def clear_print(
    value: str,
    *,
    sep: Optional[str] = None,
    end: Optional[str] = None,
    file: Optional[Any] = None,
    flush: bool = False,
) -> None:
    """
    Clear line and print
    """
    print(f"\r\x1b[K{value}", sep=sep, end=end, file=file, flush=flush)


def clear_print_clearable(
    value: str,
    *,
    sep: Optional[str] = None,
    file: Optional[Any] = None,
    flush: bool = False,
) -> None:
    """
    Clear line and print clearable
    """
    clear_print(value, sep=sep, end="", file=file, flush=flush)


def progress_str(current: int, total: int) -> str:
    """
    Generate progress string:  1/10

    Args:
        current (int): Amount finished
        total   (int): Total amount

    Returns:
        (str): Progress string:  1/10
    """
    count_str = str(total)
    return f"{current:>{len(count_str)}}/{count_str}"


def progress_percent(current: int, total: int) -> str:
    """
    Generate progress percentage:  80.785%

    Args:
        current (int): Amount finished
        total   (int): Total amount

    Returns:
        {str}: Progress percent string:  80.785%
    """
    return f"{current/total:8.3%}"


def shrink_str(shrink: str, *, prefix: str = "", postfix: str = "") -> str:
    """
    Shrink string to fit on console

    Args:
        shrink  (str): String to be shrinked
        prefix  (str): Stuff before the string that can't be shrinked
        postfix (str): Stuff after the string that can't be shrinked

    Returns:
        (str): Full string
    """
    max_len = get_terminal_size().columns - len(prefix) - len(postfix) - 4
    shrinked = ""
    counter = 0
    orig_str_iter = iter(shrink)
    while counter < max_len:
        try:
            char = next(orig_str_iter)
        except StopIteration:
            break
        counter += 1 if char.isascii() else 3
        shrinked += char
    if shrinked != shrink:
        shrink = shrinked[:-3] + "..."
    return f"{prefix} {shrink} {postfix}"
