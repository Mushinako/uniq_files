"""
Module: Walk through different types of directories

Public Constants:
    DIRECTORY_EXT: Directory extension-to-class mapping
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..zip_ import RootZipPath

if TYPE_CHECKING:
    from .type_ import UnionRootPathTypeNoDir


DIRECTORY_EXT: dict[str, UnionRootPathTypeNoDir] = {
    ".zip": RootZipPath,
}
