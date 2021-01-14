"""
Module: Common methods

Public Classes:
    BasePath (abstract): Base path abstract class
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from math import ceil
from time import time
from typing import IO, Iterator, Literal, Optional

from progbar import clear_print_clearable, shrink_str

from .utils.error import NotAFileError
from ..config import CHUNK_SIZE
from ..data.file_stat import FileStat
from ..utils.progress import ETA, Progress


class BasePath(metaclass=ABCMeta):
    """
    Base path abstract class

    Public Attributes:
        size (int):
            Size of the file/directory
        mtime (float):
            Last modified time of the file. For directories, it's not used and
            defaulted to current time
        length (int):
            Number of files under this directory, or 1 if the path is a file
        is_empty (bool):
            Whether a directory is empty

    Public Methods:
        dir_get_stats:
            Get stats of a directory
        process_dir:
            Inspect all the files in this directory and get relevant properties
        process_file:
            Inspect this file and get relevant properties
    """

    name: str
    size: int
    mtime: float
    length: int
    is_empty: bool

    filtered_dirs: list[BasePath]
    filtered_files: list[BasePath]

    _ignored_file_errors: tuple[type[Exception], ...]

    def dir_get_stats(self) -> None:
        """
        Get stats of a directory
        - size    : Sum of size of all valid subpaths
        - mtime   : Not used, current time stored to ensure difference from stored data
        - length  : Sum of length of all valid subfolders and number of files
        - is_empty: Whether the folder is empty
        """
        dir_size_total = sum(path.size for path in self.filtered_dirs)
        file_size_total = sum(path.size for path in self.filtered_files)
        self.size = dir_size_total + file_size_total
        self.mtime = time()
        dir_length_total = sum(path.length for path in self.filtered_dirs)
        self.length = dir_length_total + len(self.filtered_files)
        self.is_empty = not len(list(self.iterdir()))

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

        Args:
            existing_file_stats (dict[str, FileStat]):
                Existing path string-file property mapping
            total_progress (Progress):
                Total progress data
            eta (ETA):
                ETA data
            new_file_stats (list[FileStat]):
                Properties of all files visitied
            empty_dirs (list[UnionBasePath]):
                List of empty directories
        """
        if self.is_empty:
            empty_dirs.append(str(self))
            return

        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: {self}")

        dir_progress = Progress(len(self.filtered_files))

        for file in self.filtered_files:
            dir_progress.current += 1
            dir_progress_str = f"[{dir_progress.string}]"
            file.process_file(
                existing_file_stats,
                dir_progress_str,
                total_progress,
                eta,
                new_file_stats,
            )

        for dir_ in self.filtered_dirs:
            dir_.process_dir(
                existing_file_stats, total_progress, eta, new_file_stats, empty_dirs
            )

    def process_file(
        self,
        existing_file_stats: dict[str, FileStat],
        dir_progress_str: str,
        total_progress: Progress,
        eta: ETA,
        new_file_stats: list[FileStat],
    ) -> None:
        """
        Inspect this file and get relevant properties

        Args:
            existing_file_stats (dict[str, FileStat]):
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
        self_str = str(self)

        if not self.is_file():
            raise NotAFileError(f"Not a file: {self_str}")

        if self_str in existing_file_stats:
            existing_file_stat = existing_file_stats[self_str]

            if existing_file_stat.mtime == self.mtime:
                del existing_file_stats[self_str]

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
        except self._ignored_file_errors:
            total_progress.current += self.size
            eta.left -= self.size
            return

        new_file_stats.append(
            FileStat(str(self), self.size, self.mtime, md5_str, sha1_str)
        )

    def _hash(
        self, dir_progress_str: str, total_progress: Progress, eta: ETA
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

    @abstractmethod
    def iterdir(self) -> Iterator[BasePath]:
        raise NotImplementedError()

    @abstractmethod
    def is_dir(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_file(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def open(
        self,
        mode: Literal["rb"] = ...,
        buffering: int = ...,
        encoding: Optional[str] = ...,
        errors: Optional[str] = ...,
        newline: Optional[str] = ...,
    ) -> IO[bytes]:
        raise NotImplementedError()
