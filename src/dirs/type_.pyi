"""
Module: Main types

Public Types:
    UnionPath: A collection of the path types
"""

from typing import Union

from .dir_.type_ import DirPath
from .zip_.type_ import RootZipPath

UnionPath = Union[DirPath, RootZipPath]
