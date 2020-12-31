"""
Module: Regular directory type

Public Classes:
    DirPath
"""

from __future__ import annotations

import os
from pathlib import Path, WindowsPath, PosixPath
from typing import Any, Union


class DirPath(Path):
    """
    Similar to pathlib.Path, but works with context manager
    """

    def __new__(cls, *args: Union[str, os.PathLike[str]], **kwargs: Any) -> DirPath:
        if cls is DirPath:
            cls = _WindowsDirPath if os.name == "nt" else _PosixDirPath
        return super().__new__(cls, *args, **kwargs)

    def __enter__(self) -> DirPath:
        return self

    def __exit__(self, *_) -> None:
        pass


class _WindowsDirPath(DirPath, WindowsPath):
    pass


class _PosixDirPath(DirPath, PosixPath):
    pass
