"""
Module: Walk through different types of directories

Public Constants:
    DIRECTORY_EXT {dict[str, Callable[[pathlib.Path], Generator[tuple[str, list[Union_Path]], None, None]]]}:
        Mapping of each extension to parsing function
"""
from pathlib import Path
from typing import Callable, Dict, Generator, List, Tuple

from ..types_.dir_types import Union_Path
from .zip_ import parse_zip

DIRECTORY_EXT: Dict[
    str, Callable[[Path], Generator[Tuple[str, List[Union_Path]], None, None]]
] = {
    ".zip": parse_zip,  # type: ignore
}
