"""
Module: Zip directory type

Public Classes:
    RootZipPath
"""

from __future__ import annotations
from typing import Iterator, Union

import zipfile
from datetime import datetime
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from math import ceil
from pathlib import Path
from posixpath import dirname
from time import time
from typing import Optional

from ..config import CHUNK_SIZE
from ...config import WHITELIST
from ...file_handler.file_prop import FileProps
from ...utils.print_funcs import clear_print, shrink_str
from ...utils.time_ import CalculationTime, Progress


class _ZipPath(zipfile.Path):
    """
    Similar to `zipfile.Path`, but partly implents some file stats
    """

    # Technically `zipfile.FastLookup` but no matter
    root: zipfile.ZipFile
    at: str

    def __init__(self, root: Union[zipfile.ZipFile, zipfile.StrPath], at: str) -> None:
        super().__init__(root, at=at)
        self._zippath_init()

    def _zippath_init(self) -> None:
        """
        Add `self.size` and `self.mtime`
        """
        if self.is_file():
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
        else:
            self.size = self._size()
            self.mtime = datetime.now().timestamp()

    def _is_child_str(self, path_str: str):
        return dirname(path_str.rstrip("/")) == self.at.rstrip("/")

    def _next(self, at: str) -> _ZipPath:
        return _ZipPath(self.root, at)

    def _size(self) -> int:
        if self.is_dir():
            return sum(subpath._size() for subpath in self.iterdir())
        else:
            return self.size

    def iterdir(self) -> Iterator[_ZipPath]:
        if not self.is_dir():
            raise ValueError("Can't listdir a file")
        subs = filter(self._is_child_str, sorted(self.root.namelist()))
        return map(self._next, subs)

    def _process_dir(
        self,
        existing_file_props: Optional[FileProps],
        total_progress: Progress,
        calculation_time: CalculationTime,
        print_walking: bool = True,
    ) -> tuple[list[tuple[str, FileProps]], list[str]]:
        """
        Do `_process` on all files in a folder, recursively, and filter

        Args:
            existing_file_props (FileProps | None):
                Existing data stored in the DB
            total_progress (Progress):
                Total progresss dataclass
            calculation_time (CalculationTime):
                Data for processed calculation time
            print_walking (bool):
                Whether to print the directory walking through

        Returns:
            (list[tuple[str, FileProps]]):
                List of file name and properties that can be inferred
            (list[str]):
                List of new file file names
        """
        if print_walking:
            clear_print(f"Walking {self}...")
        files: list[_ZipPath] = []
        file_props_list: list[tuple[str, FileProps]] = []
        new_list: list[str] = []

        for subpath in self.iterdir():
            if subpath.is_dir():
                if subpath.name in WHITELIST.dirnames:
                    continue
                if str(subpath) in WHITELIST.dirpaths:
                    continue
                sub_file_props_list, sub_new_list = subpath._process_dir(
                    existing_file_props,
                    total_progress,
                    calculation_time,
                )
                file_props_list += sub_file_props_list
                new_list += sub_new_list
            else:
                if subpath.name in WHITELIST.filenames:
                    continue
                if (subpath_str := str(subpath)) in WHITELIST.filepaths:
                    continue
                if any(regex.fullmatch(subpath_str) for regex in WHITELIST.fileregexes):
                    continue
                files.append(subpath)

        progress = Progress(len(files))

        for file in files:
            progress.current += 1
            dir_progress = f"[File {progress.string}]"
            file_props, new = file._process(
                existing_file_props,
                dir_progress,
                total_progress,
                calculation_time,
            )
            if file_props is None:
                continue
            file_props_list.append((file.name, file_props))
            if new:
                new_list.append(file.name)

        return file_props_list, new_list

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


class RootZipPath(_ZipPath):
    """
    Similar to _ZipPath, but represents the root zip file, which works with
        context manager
    """

    # Technically `zipfile.FastLookup` but no matter
    root: zipfile.ZipFile
    at: str

    def __init__(self, path: Path) -> None:
        super().__init__(path, at="")
        self._path = path

    def __enter__(self) -> RootZipPath:
        if self.root.fp is None:
            return self.__class__(self._path)
        else:
            return self

    def __exit__(self, *_) -> None:
        self.root.close()

    def process(
        self,
        existing_file_props: Optional[FileProps],
        _: str,
        total_progress: Progress,
        calculation_time: CalculationTime,
    ) -> tuple[list[tuple[str, FileProps]], list[str]]:
        """
        Inspect all the files and get relevant properties

        Args:
            existing_file_props (FileProps | None):
                Existing data stored in the DB
            _ (str):
                File progress string, ignored
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
        with self:
            return self._process_dir(
                existing_file_props, total_progress, calculation_time, False
            )
