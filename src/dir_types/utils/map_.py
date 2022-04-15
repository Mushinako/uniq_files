"""
Module: Walk through different types of directories

Public Constants:
    DIRECTORY_EXT: Directory extension-to-class mapping
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.dir_types.zip_ import RootZipPath

if TYPE_CHECKING:
    _UnionRootPathTypeNoDir = type[RootZipPath]

DIRECTORY_EXT: dict[str, _UnionRootPathTypeNoDir] = {
    ".zip": RootZipPath,
}
