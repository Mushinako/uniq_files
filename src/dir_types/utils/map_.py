"""
Module: Walk through different types of directories

Public Constants:
    DIRECTORY_EXT: Directory extension-to-class mapping
"""

from __future__ import annotations

from ..zip_ import RootZipPath

_UnionRootPathTypeNoDir = type[RootZipPath]

DIRECTORY_EXT: dict[str, _UnionRootPathTypeNoDir] = {
    ".zip": RootZipPath,
}
