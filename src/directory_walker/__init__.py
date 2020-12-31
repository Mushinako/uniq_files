"""
Module: Walk through different types of directories

Public Constants:
    DIRECTORY_EXT (
        dict[str,
            tuple[
                Callable[[pathlib.Path], bool],
                Callable[[pathlib.Path], Generator[tuple[str, list[Union_Path]], None, None]]
            ]
        ]):
        Mapping of each extension to parsing function
"""
from pathlib import Path
from typing import Callable, Generator

from .zip_ import check_zip, parse_zip
from ..types_.dir_types import Union_Path

DIRECTORY_EXT: dict[
    str,
    tuple[
        Callable[[Path], bool],
        Callable[[Path], Generator[tuple[str, list[Union_Path]], None, None]],
    ],
] = {
    ".zip": (check_zip, parse_zip),
}
