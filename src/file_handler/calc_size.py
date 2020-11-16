"""
Module: Calculate total size

Public Functions:
    calc_size
"""
from __future__ import annotations
from typing import Iterator, List, Tuple

from ..utils.special_types import Union_Path


def calc_size(files_gen: Iterator[Tuple[str, List[Union_Path]]]) -> int:
    """"""