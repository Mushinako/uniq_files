"""
"""
from shutil import get_terminal_size


def progress_str(id_: int, count: int) -> str:
    """"""
    count_str = str(count)
    return f"{str(id_).rjust(len(count_str))}/{count_str}"


def process_str_len(shrink: str, *, prefix: str = "", postfix: str = "") -> int:
    """"""
    shrinked = shrink[: get_terminal_size().columns - len(prefix) - len(postfix) - 2]
    if shrinked != shrink:
        shrink = shrinked[:-3]
    return prefix + shrink + postfix
