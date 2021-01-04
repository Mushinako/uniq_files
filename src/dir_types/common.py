"""
Module: Common methods

Public Functions:
    dir_get_stats:
        Get stats of a directory
    process_dir:
        Inspect all the files in this directory and get relevant properties
    process_file_factory:
    
    hash:
        Hash the file, currently via MD5 and SHA-1
"""

from __future__ import annotations

from hashlib import md5 as md5_factory, sha1 as sha1_factory
from math import ceil
from time import time
from typing import Optional, TYPE_CHECKING

from .utils.error import NotAFileError
from ..config import CHUNK_SIZE
from ..data.file_stat import FileStat
from ..utils.print_ import clear_print_clearable, shrink_str
from ..utils.progress import ETA, Progress

if TYPE_CHECKING:
    from .utils.type_ import UnionBasePath


def dir_get_stats(self: UnionBasePath) -> None:
    """
    Get stats of a directory
     - Size         : Sum of size of all valid subpaths
     - Modified time: Not used, current time stored
     - Length       : Sum of length of all valid subfolders and number of files
    """
    dir_size_total = sum(path.size for path in self.filtered_dirs)
    file_size_total = sum(path.size for path in self.filtered_files)
    self.size = dir_size_total + file_size_total
    self.mtime = time()
    dir_length_total = sum(path.length for path in self.filtered_dirs)
    self.length = dir_length_total + len(self.filtered_files)


def process_dir(
    self: UnionBasePath,
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
        dir_.process_dir(existing_file_stats, total_progress, eta, new_file_stats)


def process_file_factory(*errors: type[Exception]):
    """
    A function that generates `process_file` method that catches corresponding
        errors
    """

    def process_file(
        self: UnionBasePath,
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
            md5_str, sha1_str = self.hash(dir_progress_str, total_progress, eta)
        except errors:
            total_progress.current += self.size
            eta.left -= self.size
            return

        new_file_stats.append(
            FileStat(str(self), self.size, self.mtime, md5_str, sha1_str)
        )

    return process_file


def hash(
    self: UnionBasePath,
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
