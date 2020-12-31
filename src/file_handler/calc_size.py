"""
Module: Calculate total size

Public Functions:
    calc_total_size
"""
from __future__ import annotations
from typing import Iterator

from ..dirs.type_ import UnionPath
from ..utils.print_funcs import clear_print, shrink_str


def calc_total_size(files_gen: Iterator[tuple[str, list[UnionPath]]]) -> int:
    """
    Calculate total size of all non-whitelisted files in the `base_path`

    Args:
        files_gen (Iterator[tuple[str, list[UnionPath]]]):
            Iterator that generates (dir_path_str, files) pairs

    Returns:
        (int): Total file size
    """
    total_size = 0

    for dir_path, files in files_gen:
        clear_print(shrink_str(dir_path), end="")
        for file in files:
            total_size += file.stat().st_size

    return total_size
