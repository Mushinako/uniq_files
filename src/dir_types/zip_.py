"""
Module: Custom path object for zip file contents

Public Classes:
    ZipPath    : Zip path
    RootZipPath: Zip path for root zip file
"""

from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path
from posixpath import dirname
from typing import Iterator, Optional

from progbar import clear_print_clearable, shrink_str

from .common import BasePath
from .utils.check_whitelist import check_dir, check_file
from .utils.error import InvalidDirectoryType
from ..data.file_stat import FileStat
from ..utils.progress import ETA, Progress


class ZipPath(zipfile.Path, BasePath):
    """
    Zip path

    Args:
        parent (RootZipPath): Root zip path object
        at     (str)        : Relative path within the zip file

    Public Attributes:
        at (str):
            Relative path within the zip file
        root (readonly zipfile.ZipFile | None):
            Actual zip file object

    Public Methods:
        iterdir:
            Emulates `zipfile.Path.iterdir`, slightly changed to avoid circular
            function calls
    """

    # `RuntimeError` is raised when the file is encrypted
    _ignored_file_errors = (PermissionError, RuntimeError)

    def __init__(self, parent: RootZipPath, at: str) -> None:
        self._parent = parent
        self.at = at
        self._zipfile_init()

    @property
    def root(self) -> Optional[zipfile.ZipFile]:
        return self._parent.root_fp

    def _zipfile_init(self) -> None:
        """
        Initialization
         - Filter paths
         - Get file stats
        """
        clear_print_clearable(shrink_str(str(self)))
        self.filtered_dirs: list[ZipPath] = []
        self.filtered_files: list[ZipPath] = []
        self._filter_paths()
        self._get_stats()

    def _filter_paths(self) -> None:
        """
        Filter subpaths and store them in `self._filtered_paths`
        """
        if not self.is_dir():
            return

        for subpath in self.iterdir():
            if subpath.is_dir():
                if check_dir(subpath):
                    self.filtered_dirs.append(subpath)

            else:
                if check_file(subpath):
                    self.filtered_files.append(subpath)

    def _get_stats(self) -> None:
        """
        Get file stats and store them in `self.size` and `self.mtime`
        """
        if self.is_dir():
            self.dir_get_stats()
        else:
            if self.root is None:
                raise ValueError("Can't iterdir a closed zip file")
            info = self.root.getinfo(self.at)
            self.size = info.file_size
            date_time = (
                info.date_time[0],
                month if (month := info.date_time[1]) else 1,
                day if (day := info.date_time[2]) else 1,
                info.date_time[3],
                info.date_time[4],
                info.date_time[5],
            )
            self.mtime = datetime(*date_time).timestamp()
            self.length = 1

    def iterdir(self) -> Iterator[ZipPath]:
        """
        Emulates `zipfile.Path.iterdir`, slightly changed to avoid circular
            function calls
        """
        if not self.is_dir():
            raise ValueError("Can't listdir a file")
        if self.root is None:
            raise ValueError("Can't iterdir a closed zip file")
        subs = filter(self._is_child_str, sorted(self.root.namelist()))
        return map(self._next, subs)

    def _next(self, at: str) -> ZipPath:
        return ZipPath(self._parent, at)

    def _is_child_str(self, path_str: str):
        return dirname(path_str.rstrip("/")) == self.at.rstrip("/")


class RootZipPath(ZipPath):
    """
    Zip path for root zip file

    Args:
        path (pathlib.Path):
            Path of the file/directory
        test (bool):
            Whether the zip file is creatd for test purposes. If so, only create
            a minimal zip file to see if it can be opened

    Public Attributes:
        root_fp (zipfile.ZipFile | None):
            Actual zip file object
        at (str):
            Relative path within the zip file; always "" (empty string)
        size (int):
            Size of the file/directory
        mtime (float):
            Last modified time of the file. For directories, it's not used and
            defaulted to current time
        root (readonly zipfile.ZipFile | None):
            Actual zip file object, points to `self.root_fp`

    Public Methods:
        process_dir:
            Inspect all the files in this directory and get relevant properties;
            added step to open zip file
    """

    def __init__(self, path: Path, test: bool = False) -> None:
        self._path = path
        self.root_fp: Optional[zipfile.ZipFile] = None
        if test:
            try:
                with self:
                    pass
            except (zipfile.BadZipFile, NotImplementedError, FileNotFoundError) as err:
                raise InvalidDirectoryType from err
            return
        self._parent = self
        self.at = ""
        with self:
            self._zipfile_init()

    def __enter__(self) -> RootZipPath:
        self.root_fp = self._make()
        return self

    def __exit__(self, *_) -> None:
        if self.root_fp is None:
            return
        self.root_fp.close()
        self.root_fp = None

    def process_dir(
        self,
        existing_file_stats: dict[str, FileStat],
        total_progress: Progress,
        eta: ETA,
        new_file_stats: list[FileStat],
        empty_dirs: list[str],
    ) -> None:
        """
        Inspect all the files in this directory and get relevant properties
        """
        try:
            with self:
                super().process_dir(
                    existing_file_stats, total_progress, eta, new_file_stats, empty_dirs
                )
        except FileNotFoundError:
            # The file may have been deleted since then
            total_progress.current += self.size
            eta.left -= self.size

    def _make(self) -> zipfile.ZipFile:
        """
        Open the zipfile
        """
        return zipfile.FastLookup.make(self._path)  # type: ignore
