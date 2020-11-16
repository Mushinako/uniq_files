"""
Module: Special file properties stuff

Public Classes:
    Path_Type
    File_Props

Public Constants:
    PATH_FUNCTION_MAP
"""
from __future__ import annotations
import pathlib
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict

from ..types_.dir_types import Union_Path, Zip_Path


class Path_Type(Enum):
    """
    Path type to `int` mapping
    """

    REGULAR = 0
    ZIPPED = 1


@dataclass
class File_Props:
    """
    File properties

    Properties:
        path {Union_Path}: Path of the file
        path_type {_Path_Type}
    """

    path: Union_Path
    path_type: Path_Type
    size: int
    last_modified: float
    md5: str
    sha1: str


PATH_CLASS_MAP: Dict[Path_Type, Any] = {
    Path_Type.REGULAR: pathlib.Path,
    Path_Type.ZIPPED: Zip_Path,
}
