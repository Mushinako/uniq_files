"""
Module: Inspect file properties
"""
from __future__ import annotations
from typing import Iterator, List, Tuple

from ..types_.dir_types import Union_Path


def inspect_files(files_gen: Iterator[Tuple[str, List[Union_Path]]]):
    """"""