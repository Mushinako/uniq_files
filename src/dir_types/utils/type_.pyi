"""
Module: Common types

Public Types:
    UnionBasePath:
        A collection of the base path types
    UnionRootPath:
        A collection of the root path types
    UnionRootPathTypeNoDir:
        A collection of the root path class types, not including `DirPath`
"""

from typing import Union

from ..dir_ import DirPath
from ..zip_ import RootZipPath, ZipPath

UnionBasePath = Union[DirPath, ZipPath]
UnionRootPath = Union[DirPath, RootZipPath]
UnionRootPathTypeNoDir = type[RootZipPath]
