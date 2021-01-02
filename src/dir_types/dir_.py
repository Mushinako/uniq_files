"""
Module: Custom path object for regular

Public Classes:
    DirPath: Regular path (Directory)
"""

from __future__ import annotations

import os
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from math import ceil
from pathlib import Path, WindowsPath, PosixPath
from time import time
from typing import Optional, TYPE_CHECKING

from .utils.check_whitelist import check_dir, check_file
from .utils.error import InvalidDirectoryType, NotAFileError
from .utils.map_ import DIRECTORY_EXT
from ..config import CHUNK_SIZE
from ..data.file_stat import FileStat
from ..utils.print_ import clear_print_clearable, shrink_str
from ..utils.progress import ETA, Progress

if TYPE_CHECKING:
    from .utils.type_ import UnionRootPath


class DirPath(Path):
    """
    Regular path (Directory)

    Args:
        path (pathlib.Path): Path of the file/directory

    Public Attributes:
        path (pathlib.Path):
            Path of the file/directory
        size (int):
            Size of the file/directory
        mtime (float):
            Last modified time of the file. For directories, it's not used and
            defaulted to current time

    Public Methods:
        process_dir:
            Inspect all the files in this directory and get relevant properties
        process_file:
            Inspect this file and get relevant properties
    """

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
        self._filtered_dirs: list[UnionRootPath] = []
        self._filtered_files: list[DirPath] = []
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
                        self._filtered_dirs.append(self.__class__(subpath))
                    continue

                if (cls := DIRECTORY_EXT.get(subpath.suffix)) is not None:
                    try:
                        cls(subpath, test=True)
                    except InvalidDirectoryType:
                        # Treat file as regular file if cannot be read correctly
                        pass
                    else:
                        if check_dir(subpath):
                            self._filtered_dirs.append(cls(subpath))
                        continue

                if subpath.is_file():
                    if check_file(subpath):
                        self._filtered_files.append(self.__class__(subpath))
                    continue

        except PermissionError:
            return

    def _get_stats(self) -> None:
        """
        Get file stats and store them in `self.size` and `self.mtime`
        """
        if self.is_dir():
            dir_size_total = sum(path.size for path in self._filtered_dirs)
            file_size_total = sum(path.size for path in self._filtered_files)
            self.size = dir_size_total + file_size_total
            self.mtime = time()
        elif self.is_file():
            stats = self.stat()
            self.size = stats.st_size
            self.mtime = stats.st_mtime

    def process_dir(
        self,
        existing_file_stats: dict[str, FileStat],
        total_progress: Progress,
        eta: ETA,
    ) -> tuple[list[FileStat], list[str]]:
        """
        Inspect all the files in this directory and get relevant properties

        Args:
            existing_file_stats (dict[str, FileStat]):
                Existing path string-file property mapping
            total_progress (Progress):
                Total progress data
            eta (ETA):
                ETA data

        Returns:
            (list[FileStat]): Properties of all files under this folder
            (list[str])     : All new file path strings
        """
        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: {self}")

        file_stats: list[FileStat] = []
        new_path_strs: list[str] = []

        dir_progress = Progress(len(self._filtered_files))

        for file in self._filtered_files:
            dir_progress.current += 1
            existing_file_stat = existing_file_stats.get(str(file))
            dir_progress_str = f"[{dir_progress.string}]"
            file_stat, is_new = file.process_file(
                existing_file_stat, dir_progress_str, total_progress, eta
            )
            if file_stat is None:
                continue
            file_stats.append(file_stat)
            if is_new:
                new_path_strs.append(str(self))

        for dir_ in self._filtered_dirs:
            sub_file_stats, sub_new_path_strs = dir_.process_dir(
                existing_file_stats, total_progress, eta
            )
            file_stats += sub_file_stats
            new_path_strs += sub_new_path_strs

        return file_stats, new_path_strs

    def process_file(
        self,
        existing_file_stat: Optional[FileStat],
        dir_progress_str: str,
        total_progress: Progress,
        eta: ETA,
    ) -> tuple[Optional[FileStat], bool]:
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

        Returns:
            (FileStat | None): Properties of this file, if can be inferred
            (bool)           : Whether the file is new
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

            return existing_file_stat, False

        try:
            md5_str, sha1_str = self._hash(dir_progress_str, total_progress, eta)
        except PermissionError:
            total_progress.current += self.size
            eta.left -= self.size
            return None, False

        return FileStat(str(self), self.size, self.mtime, md5_str, sha1_str), True

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


class _WindowsDirPath(DirPath, WindowsPath):
    """
    Windows version of DirPath
    """


class _PosixDirPath(DirPath, PosixPath):
    """
    Posix version of DirPath
    """
