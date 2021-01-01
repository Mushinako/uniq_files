"""
Module: Regular directory type

Public Classes:
    DirPath
"""

from __future__ import annotations

import os
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from math import ceil
from pathlib import Path, WindowsPath, PosixPath
from time import time
from typing import Any, Optional, Union

from ..config import CHUNK_SIZE
from ...file_handler.file_prop import FileProps
from ...utils.print_funcs import clear_print, shrink_str
from ...utils.time_ import CalculationTime, Progress


class DirPath(Path):
    """
    Similar to pathlib.Path, but implements content hashing
    """

    def __new__(cls, *args: Union[str, os.PathLike[str]], **kwargs: Any) -> DirPath:
        if cls is DirPath:
            cls = _WindowsDirPath if os.name == "nt" else _PosixDirPath
        self = super().__new__(cls, *args, **kwargs)
        self._dirpath_init()
        return self

    def _dirpath_init(self) -> None:
        """
        Add `self.size` and `self.mtime`
        """
        stats = self.stat()
        self.size = stats.st_size
        self.mtime = stats.st_mtime

    def process(
        self,
        existing_file_props: Optional[FileProps],
        dir_progress: str,
        total_progress: Progress,
        calculation_time: CalculationTime,
    ) -> tuple[list[tuple[str, FileProps]], list[str]]:
        """
        Inspect all the files and get relevant properties

        Args:
            existing_file_props (FileProps | None):
                Existing data stored in the DB
            file_progress (str):
                File progress string
            total_progress (Progress):
                Total progresss dataclass
            calculation_time (CalculationTime):
                Data for processed calculation time

        Returns:
            (list[tuple[str, FileProps]]):
                File name and properties, if can be inferred
            (list[str]):
                File name, if the file is new
        """
        file_props, new = self._process(
            existing_file_props, dir_progress, total_progress, calculation_time
        )
        if file_props is None:
            return [], []
        elif new:
            return [(self.name, file_props)], [self.name]
        else:
            return [(self.name, file_props)], []

    def _process(
        self,
        existing_file_props: Optional[FileProps],
        dir_progress: str,
        total_progress: Progress,
        calculation_time: CalculationTime,
    ) -> tuple[Optional[FileProps], bool]:
        """
        Inspect all the files and get relevant properties

        Args:
            existing_file_props (FileProps | None):
                Existing data stored in the DB
            dir_progress (str):
                Directory progress string
            total_progress (Progress):
                Total progresss dataclass
            calculation_time (CalculationTime):
                Data for processed calculation time

        Returns:
            (FileProps | None): File properties of a file, if can be inferred
            (bool)            : Whether the file is new
        """
        if not self.is_file():
            return None, False

        if existing_file_props is not None and existing_file_props.mtime == self.mtime:
            total_progress.current += self.size
            calculation_time.left -= self.size
            clear_print(
                shrink_str(
                    self.name,
                    prefix=f"{total_progress.percentage} {dir_progress}",
                    postfix=calculation_time.time_left,
                ),
                end="",
            )
            return existing_file_props, False

        try:
            md5, sha1 = self._hash(dir_progress, total_progress, calculation_time)
        except PermissionError:
            total_progress.current += self.size
            return None, False
        return (
            FileProps(str(self), self.size, self.mtime, md5, sha1),
            True,
        )

    def _hash(
        self,
        dir_progress: str,
        total_progress: Progress,
        calculation_time: CalculationTime,
    ):
        """
        Hash the file, currently via MD5 and SHA-1

        Args:
            dir_progress     (str)            : Directory progress
            total_progress   (Progress)       : Overall progress
            calculation_time (CalculationTime): Calculation time data

        Returns:
            (str): MD5 hash
            (str): SHA-1 hash
        """
        md5 = md5_factory()
        sha1 = sha1_factory()

        num_chunks = ceil(self.size / CHUNK_SIZE)

        with self.open("rb") as fp:
            chunk_progress = Progress(num_chunks)
            for _ in range(num_chunks):
                start = time()
                chunk = fp.read(CHUNK_SIZE)
                md5.update(chunk)
                sha1.update(chunk)
                chunk_size = len(chunk)
                chunk_progress.current += 1
                total_progress.current += chunk_size
                calculation_time.left -= chunk_size
                calculation_time.processed += chunk_size
                calculation_time.time_taken += time() - start
                clear_print(
                    shrink_str(
                        self.name,
                        prefix=f"{total_progress.percentage} {dir_progress}",
                        postfix=f"[Chunk {chunk_progress.string}] {calculation_time.time_left}",
                    ),
                    end="",
                )

        return md5.hexdigest(), sha1.hexdigest()


class _WindowsDirPath(DirPath, WindowsPath):
    pass


class _PosixDirPath(DirPath, PosixPath):
    pass
