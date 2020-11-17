"""
Module: Helper functions

Public Functions:
    clear_print
    progress_str
    progress_percent
    shrink_str
"""
from __future__ import annotations
from shutil import get_terminal_size
from typing import Any, Optional


def clear_print(
    print_text: str,
    *,
    sep: Optional[str] = None,
    end: Optional[str] = None,
    file: Optional[Any] = None,
    flush: bool = False,
) -> None:
    """
    Clear line and print
    """
    print("\r\x1b[K" + print_text, sep=sep, end=end, file=file, flush=flush)


def progress_str(id_: int, count: int) -> str:
    """
    Generate progress string:  1/10

    Args:
        id_   {int}: ID of current element
        count {int}: Number of total elements

    Returns:
        {str}: Progress string:  1/10
    """
    count_str = str(count)
    return f"{id_:>{len(count_str)}}/{count_str}"


def progress_percent(finished_size: int, total_size: int) -> str:
    """
    Generate progress percentage:  80.785%

    Args:
        finished_size {int}: The cumulative size of finished stuff
        total_size    {int}: The total size of stuff

    Returns:
        {str}: Progress percent string:  80.785%
    """
    return f"{finished_size/total_size:8.3%}"


def shrink_str(shrink: str, *, prefix: str = "", postfix: str = "") -> str:
    """
    Shrink string to fit on console

    Args:
        shrink  {str}: String to be shrinked
        prefix  {str}: Stuff before the string that can't be shrinked
        postfix {str}: Stuff after the string that can't be shrinked

    Returns:
        {str}: Full string
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
        if char.isascii():
            counter += 1
        else:
            counter += 2
        shrinked += char
    if shrinked != shrink:
        shrink = shrinked[:-3] + "..."
    return f"{prefix} {shrink} {postfix}"
