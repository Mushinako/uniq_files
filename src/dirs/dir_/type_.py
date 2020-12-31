"""
Module: Regular directory type

Public Classes:
    DirPath
"""

from __future__ import annotations

from pathlib import Path


class DirPath(Path):
    """
    Similar to pathlib.Path, but works with context manager
    """

    def __enter__(self) -> DirPath:
        return self

    def __exit__(self, *_) -> None:
        pass
