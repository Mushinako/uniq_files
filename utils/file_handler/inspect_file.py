"""
Module: Inspect each file and get information

Public Classes:
    Path_Type
    File_Props
"""
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass

from ..utils.special_types import Union_Path


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
    path_type: int
    size: int
    last_modified: float
    md5: str
    sha1: str