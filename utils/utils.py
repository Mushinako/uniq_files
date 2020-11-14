"""
"""
from shutil import get_terminal_size


def progress_str(id_: int, count: int) -> str:
    """"""
    count_str = str(count)
    return str(id_).rjust(len(count_str)) + "/" + str(count_str)


def progress_percent(finished_size: int, total_size: int) -> str:
    """"""
    return f"{finished_size/total_size:8.3%} "


def process_str_len(shrink: str, *, prefix: str = "", postfix: str = "") -> str:
    """"""
    shrinked = shrink[: get_terminal_size().columns - len(prefix) - len(postfix) - 4]
    if shrinked != shrink:
        shrink = shrinked[:-3] + "..."
    return "\r\x1b[K" + prefix + shrink + postfix
