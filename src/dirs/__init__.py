"""
Module: Walk through different types of directories

Public Constants:
    DIRECTORY_EXT
"""
from pathlib import Path
from typing import Callable, Generator

from .type_ import UnionPath
from .zip_.walker import check_zip, parse_zip


DIRECTORY_EXT: dict[
    str,
    tuple[
        Callable[[Path], bool],
        Callable[[Path], Generator[tuple[str, list[UnionPath]], None, None]],
    ],
] = {
    ".zip": (check_zip, parse_zip),
}
