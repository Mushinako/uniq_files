"""
Module: Special file properties stuff

Public Classes:
    Path_Type
    File_Props

Public Functions:
    class_2_type

Public Constants:
    PATH_CLASS_MAP
"""
from __future__ import annotations
from pathlib import Path, WindowsPath, PosixPath
from enum import Enum
from dataclasses import dataclass
from typing import Callable

from ..types_.dir_types import Union_Path, Union_Path_Types, Zip_Path


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


PATH_CLASS_MAP: dict[Path_Type, Callable[[str], Union_Path]] = {
    Path_Type.REGULAR: Path,
    Path_Type.ZIPPED: Zip_Path.from_zip_path,
}


def class_2_type(cls: Union_Path_Types) -> Path_Type:
    """
    Reverse of the `PATH_CLASS_MAP` mapping get method

    Args:
        cls {Union[Type[Path], Type[Zip_Path]]}: The class to be checked

    Returns:
        {Path_Type}: Corresponding path type
    """
    for path_type, path_cls in PATH_CLASS_MAP.items():
        if cls in (WindowsPath, PosixPath):
            cls = Path
        if path_cls == cls:
            return path_type
    raise ValueError(f"{cls.__name__} is not a valid class.")