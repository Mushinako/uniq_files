"""
Module: Inspect each file and get information

Public Classes:
    Path_Type
    File_Props

Public Constants:
    PATH_FUNCTION_MAP
"""
from __future__ import annotations
import pathlib
import zipfile
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Type

from ..utils.special_types import Union_Path


class Path_Type(Enum):
    """
    Path type to `int` mapping
    """

    REGULAR = 0
    ZIPPED = 1


PATH_CLASS_MAP: Dict[Path_Type, Type[Union_Path]] = {
    Path_Type.REGULAR: pathlib.Path,
    Path_Type.ZIPPED: zipfile.Path,
}


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