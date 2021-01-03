"""
Module: Custom path object for zip file contents

Public Classes:
    ZipPath    : Zip path
    RootZipPath: Zip path for root zip file
"""

from __future__ import annotations
from typing import Iterator, Optional

import zipfile
from datetime import datetime
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from math import ceil
from pathlib import Path
from posixpath import dirname
from time import time

from .utils.check_whitelist import check_dir, check_file
from .utils.error import InvalidDirectoryType, NotAFileError
from ..config import CHUNK_SIZE
from ..data.file_stat import FileStat
from ..utils.print_ import clear_print_clearable, shrink_str
from ..utils.progress import ETA, Progress


class ZipPath(zipfile.Path):
    """
    Zip path

    Args:
        parent (RootZipPath): Root zip path object
        at     (str)        : Relative path within the zip file

    Public Attributes:
        at (str):
            Relative path within the zip file
        size (int):
            Size of the file/directory
        mtime (float):
            Last modified time of the file. For directories, it's not used and
            defaulted to current time
        length (int):
            Number of files under this directory, or 1 if the path is a file
        root (readonly zipfile.ZipFile | None):
            Actual zip file object

    Public Methods:
        process_dir:
            Inspect all the files in this directory and get relevant properties
        process_file:
            Inspect this file and get relevant properties
        iterdir:
            Emulates `zipfile.Path.iterdir`, slightly changed to avoid circular
            function calls
    """

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
        self._filtered_dirs: list[ZipPath] = []
        self._filtered_files: list[ZipPath] = []
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
                    self._filtered_dirs.append(subpath)

            else:
                if check_file(subpath):
                    self._filtered_files.append(subpath)

    def _get_stats(self) -> None:
        """
        Get file stats and store them in `self.size` and `self.mtime`
        """
        if self.is_dir():
            dir_size_total = sum(path.size for path in self._filtered_dirs)
            file_size_total = sum(path.size for path in self._filtered_files)
            self.size = dir_size_total + file_size_total
            self.mtime = time()
            dir_length_total = sum(path.length for path in self._filtered_dirs)
            self.length = dir_length_total + len(self._filtered_files)
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

    def process_dir(
        self,
        existing_file_stats: dict[str, FileStat],
        total_progress: Progress,
        eta: ETA,
        new_file_stats: list[FileStat],
    ) -> None:
        """
        Inspect all the files in this directory and get relevant properties

        Args:
            existing_file_stats (dict[str, FileStat]):
                Existing path string-file property mapping
            total_progress (Progress):
                Total progress data
            eta (ETA):
                ETA data
            new_file_stats (list[FileStat]):
                Properties of all files visitied
        """
        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: {self}")

        dir_progress = Progress(len(self._filtered_files))

        for file in self._filtered_files:
            dir_progress.current += 1
            existing_file_stat = existing_file_stats.pop(str(file), None)
            dir_progress_str = f"[{dir_progress.string}]"
            file.process_file(
                existing_file_stat,
                dir_progress_str,
                total_progress,
                eta,
                new_file_stats,
            )

        for dir_ in self._filtered_dirs:
            dir_.process_dir(existing_file_stats, total_progress, eta, new_file_stats)

    def process_file(
        self,
        existing_file_stat: Optional[FileStat],
        dir_progress_str: str,
        total_progress: Progress,
        eta: ETA,
        new_file_stats: list[FileStat],
    ) -> None:
        """
        Inspect this file and get relevant properties

        Args:
            existing_file_stats (FileStat | None):
                Existing path string-file property mapping
            dir_progress_str (str):
                Directory progress data, formatted string
            total_progress (Progress):
                Total progress data
            eta (ETA):
                ETA data
            new_file_stats (list[FileStat]):
                Properties of all files visitied
        """
        if not self.is_file():
            raise NotAFileError(f"Not a file: {self}")

        if existing_file_stat is not None and existing_file_stat.mtime == self.mtime:
            total_progress.current += self.size
            eta.left -= self.size

            clear_print_clearable(
                shrink_str(
                    str(self),
                    prefix=f"{total_progress.percent} {eta.string} {dir_progress_str}",
                )
            )

            return

        try:
            md5_str, sha1_str = self._hash(dir_progress_str, total_progress, eta)
        except (PermissionError, RuntimeError):
            # `RuntimeError` for encrypted files
            total_progress.current += self.size
            eta.left -= self.size
            return

        new_file_stats.append(
            FileStat(str(self), self.size, self.mtime, md5_str, sha1_str)
        )

    def _hash(
        self,
        dir_progress_str: str,
        total_progress: Progress,
        eta: ETA,
    ) -> tuple[str, str]:
        """
        Hash the file, currently via MD5 and SHA-1

        Args:
            dir_progress_str (str)     : Directory progress data, formatted string
            total_progress   (Progress): Total progress data
            eta              (ETA)     : ETA data

        Returns:
            (str): MD5 hash hex
            (str): SHA-1 hash hex
        """
        md5 = md5_factory()
        sha1 = sha1_factory()

        num_chunks = ceil(self.size / CHUNK_SIZE)
        chunk_progress = Progress(num_chunks)

        with self.open("rb") as fp:
            for _ in range(num_chunks):
                start = time()

                chunk = fp.read(CHUNK_SIZE)
                md5.update(chunk)
                sha1.update(chunk)

                chunk_size = len(chunk)
                chunk_progress.current += 1
                total_progress.current += chunk_size
                eta.left -= chunk_size
                eta.processed += chunk_size
                eta.time_taken += time() - start

                clear_print_clearable(
                    shrink_str(
                        str(self),
                        prefix=(
                            f"{total_progress.percent} {eta.string} "
                            f"{dir_progress_str} [Chunk {chunk_progress.string}]"
                        ),
                    )
                )

        return md5.hexdigest(), sha1.hexdigest()

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
    ) -> None:
        """
        Inspect all the files in this directory and get relevant properties

        Args:
            existing_file_stats (dict[str, FileStat]):
                Existing path string-file property mapping
            total_progress (Progress):
                Total progress data
            eta (ETA):
                ETA data
            new_file_stats (list[FileStat]):
                Properties of all files visitied
        """
        try:
            with self:
                super().process_dir(
                    existing_file_stats, total_progress, eta, new_file_stats
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
