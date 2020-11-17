"""
Module: Calculate total size

Public Functions:
    calc_total_size
"""
from __future__ import annotations
from typing import Iterator, List, Tuple

from ..utils.print_funcs import clear_print, shrink_str
from ..types_.dir_types import Union_Path


def calc_total_size(files_gen: Iterator[Tuple[str, List[Union_Path]]]) -> int:
    """
    Calculate total size of all non-whitelisted files in the `base_path`

    Args:
        files_gen {Iterator[tuple[str, list[Union_Path]]]}:
            Iterator that generates (dir_path, files) pairs

    Returns:
        {int}: Total file size
    """
    total_size = 0

    for dir_path, files in files_gen:
        clear_print(shrink_str(dir_path), end="")
        for file in files:
            total_size += file.stat().st_size

    return total_size