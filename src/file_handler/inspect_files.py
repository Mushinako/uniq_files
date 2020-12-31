"""
Module: Inspect file properties

Public Functions:
    inspect_all_files
"""
from __future__ import annotations
from math import ceil
from time import time
from traceback import print_exc
from collections import defaultdict
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from typing import Iterator, Optional

from .file_prop import FileProps
from ..utils.print_funcs import clear_print, shrink_str
from ..dirs.type_ import UnionPath
from ..utils.time_ import CalculationTime, Progress

_CHUNK_SIZE = 1 << 26  # 64 MiB


def inspect_all_files(
    files_gen: Iterator[tuple[str, list[UnionPath]]],
    db_data: dict[str, FileProps],
    total_size: int,
) -> tuple[list[tuple[tuple[int, str, str], list[str]]], list[FileProps], list[str]]:
    """
    Inspect all the files and get relevant properties

    Args:
        files_gen  (Iterator[tuple[str, list[UnionPath]]]):
            Iterator that generates (dir_path_str, files) pairs
        db_data    (dict[str, FileProps]):
            Existing path string-file property mapping
        total_size (int):
            Total size of all files

    Returns:
        (list[tuple[tuple[int, str, str], list[str]]]):
            All duplications
        (list[FileProps]):
            All file properties
        (list[str]):
            All new files
    """
    same_props: defaultdict[tuple[int, str, str], list[str]] = defaultdict(list)
    files_props: list[FileProps] = []
    new_files: list[str] = []

    files = tuple(files_gen)

    calculation_time = CalculationTime(total_size)
    total_progress = Progress(total_size)

    try:
        for dir_path, file_paths in files:
            clear_print(f"Walking {dir_path}...")
            progress = Progress(len(file_paths))
            for file_path in file_paths:
                progress.current += 1
                dir_progress = f"[File {progress.string}]"
                file_props, new = _inspect_file(
                    file_path,
                    db_data.get(str(file_path)),
                    dir_progress,
                    total_progress,
                    calculation_time,
                )
                if file_props is None:
                    continue
                same_props[file_props.size, file_props.md5, file_props.sha1].append(
                    str(file_path)
                )
                if new:
                    new_files.append(str(file_path))
                files_props.append(file_props)
    except KeyboardInterrupt:
        clear_print("Stopping...")
    except Exception:
        print_exc()

    dup_list = [entry for entry in sorted(same_props.items()) if len(entry) > 1]

    return dup_list, files_props, new_files


def _inspect_file(
    file_path: UnionPath,
    existing_file_props: Optional[FileProps],
    dir_progress: str,
    total_progress: Progress,
    calculation_time: CalculationTime,
) -> tuple[Optional[FileProps], bool]:
    """
    Inspect all the files and get relevant properties

    Args:
        file_path (Union_Path):
            Get file properties for file at path
        existing_file_props (FileProps | None):
            Existing data stored in the DB
        file_progress (str):
            File progress string
        total_progress (Progress):
            Total progresss dataclass
        calculation_time (CalculationTime):
            Data for processed calculation time

    Returns:
        (FileProps | None): File properties of a file, if can be inferred
        (bool)            : Whether the file is new
    """
    stats = file_path.stat()
    size = stats.st_size
    last_modified = stats.st_mtime

    if (
        existing_file_props is not None
        and existing_file_props.last_modified == last_modified
    ):
        total_progress.current += size
        calculation_time.left -= size
        clear_print(
            shrink_str(
                file_path.name,
                prefix=f"{total_progress.percentage} {dir_progress}",
                postfix=calculation_time.time_left,
            ),
            end="",
        )
        return existing_file_props, False

    num_chunks = ceil(size / _CHUNK_SIZE)

    md5 = md5_factory()
    sha1 = sha1_factory()

    try:
        with file_path.open("rb") as fp:
            chunk_progress = Progress(num_chunks)
            for _ in range(num_chunks):
                start = time()
                chunk = fp.read(_CHUNK_SIZE)
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
                        file_path.name,
                        prefix=f"{total_progress.percentage} {dir_progress}",
                        postfix=f"[Chunk {chunk_progress.string}] {calculation_time.time_left}",
                    ),
                    end="",
                )
    except PermissionError:
        total_progress.current += file_path.stat().st_size
        return None, False
    else:
        return (
            FileProps(
                str(file_path),
                size,
                last_modified,
                md5.hexdigest(),
                sha1.hexdigest(),
            ),
            True,
        )
