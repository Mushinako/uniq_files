"""
Module: Calculate total size

Public Functions:
    calc_total_size
"""
from __future__ import annotations
from typing import Iterator

from ..dirs.type_ import UnionPath


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

    for _, files in files_gen:
        for file in files:
            total_size += file.size

    return total_size
