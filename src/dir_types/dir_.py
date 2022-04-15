"""
Module: Custom path object for regular

Public Classes:
    DirPath: Regular path (Directory)
"""

from __future__ import annotations

import os
from pathlib import Path, WindowsPath, PosixPath
from typing import TYPE_CHECKING

from progbar import clear_print_clearable, shrink_str

from .common import BasePath
from .utils.check_whitelist import check_dir, check_file
from .utils.error import InvalidDirectoryType
from .utils.map_ import DIRECTORY_EXT

if TYPE_CHECKING:
    from typing import IO, Iterator


class DirPath(BasePath, Path):
    """
    Regular path (Directory)

    Args:
        path (pathlib.Path): Path of the file/directory
    """

    _ignored_file_errors = (PermissionError, FileNotFoundError)

    def __new__(cls, path: Path) -> DirPath:
        """
        Make special subclasses depending on OS
        """
        if cls is DirPath:
            cls = _WindowsDirPath if os.name == "nt" else _PosixDirPath
        self = super().__new__(cls, path)
        self._dirpath_init()
        return self

    def _dirpath_init(self) -> None:
        """
        Initialization
         - Filter paths
         - Get file stats
        """
        clear_print_clearable(shrink_str(str(self)))
        self.filtered_dirs = []
        self.filtered_files = []
        self._filter_paths()
        self._get_stats()

    def _filter_paths(self) -> None:
        """
        Filter subpaths and store them in `self._filtered_paths`
        """
        if not self.is_dir():
            return

        try:
            for subpath in sorted(self.iterdir()):
                if subpath.is_dir():
                    if check_dir(subpath):
                        self.filtered_dirs.append(self.__class__(subpath))
                    continue

                if (cls := DIRECTORY_EXT.get(subpath.suffix)) is not None:
                    try:
                        cls(subpath, test=True)
                    except InvalidDirectoryType:
                        # Treat file as regular file if cannot be read correctly
                        pass
                    else:
                        if check_dir(subpath):
                            self.filtered_dirs.append(cls(subpath))
                        continue

                if subpath.is_file():
                    if check_file(subpath):
                        self.filtered_files.append(self.__class__(subpath))
                    continue

        except PermissionError:
            return

    def _get_stats(self) -> None:
        """
        Get file stats and store them in `self.size` and `self.mtime`
        """
        if self.is_dir():
            self.dir_get_stats()
        elif self.is_file():
            stats = self.stat()
            self.size = stats.st_size
            self.mtime = stats.st_mtime
            self.length = 1
            self.is_empty = False

    def iter(self) -> Iterator[Path]:
        return self.iterdir()

    def is_dir_(self) -> bool:
        return self.is_dir()

    def is_file_(self) -> bool:
        return self.is_file()

    def open_file(self) -> IO[bytes]:
        return self.open("rb")

    @property
    def name_(self) -> str:
        return self.name


class _WindowsDirPath(DirPath, WindowsPath):
    """
    Windows version of DirPath
    """


class _PosixDirPath(DirPath, PosixPath):
    """
    Posix version of DirPath
    """
