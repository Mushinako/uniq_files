"""
Module: Reading from and writing to sqlite3 database

Public Functions:
    read_db  {Path -> dict[Path, File_Props]}
    write_db {Path, list[File_Props] -> None}
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List

from ..utils.special_types import Union_Path
from ..file_handler.inspect_file import File_Props


def read_db(path: Path) -> Dict[Union_Path, File_Props]:
    """
    Read database at given path and returns data in a dictionary

    Args:
        path {Path}
    """


def write_db(path: Path, files_props: List[File_Props]) -> None:
    """"""