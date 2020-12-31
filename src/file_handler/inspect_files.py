"""
Module: Inspect file properties

Public Functions:
    inspect_all_files
"""
from __future__ import annotations
from math import ceil
from time import time
from collections import defaultdict
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from typing import Iterator, Optional

from ..utils.print_funcs import clear_print, progress_percent, progress_str, shrink_str
from ..types_.dir_types import Union_Path
from ..types_.file_prop import File_Props
from ..utils.time_ import CalculationTime, time_remaining

_CHUNK_SIZE = 1 << 26  # 64 MiB


def inspect_all_files(
    files_gen: Iterator[tuple[str, list[Union_Path]]],
    db_data: dict[str, File_Props],
    total_size: int,
) -> tuple[list[tuple[tuple[int, str, str], list[str]]], list[File_Props], list[str]]:
    """
    Inspect all the files and get relevant properties

    Args:
        files_gen  {Iterator[tuple[str, list[Union_Path]]]}:
            Iterator that generates (dir_path, files) pairs
        db_data    {dict[str, File_Props]}:
            Existing path-file property mapping
        total_size {int}:
            Total size of all files

    Returns:
        {list[tuple[tuple[int, str, str], list[str]]]}: All duplications
        {list[File_Props]}                            : All file properties
        {list[str]}                                   : All new files
    """
    same_props: defaultdict[tuple[int, str, str], list[str]] = defaultdict(list)
    files_props: list[File_Props] = []
    new_files: list[str] = []
    finished_size = 0

    files = tuple(files_gen)

    calculation_time = CalculationTime(len(files))

    try:
        for dir_path, file_paths in files:
            clear_print(f"Walking {dir_path}...")
            num_files = len(file_paths)
            for i, file_path in enumerate(file_paths):
                dir_progress = f"[File {progress_str(i+1, num_files)}]"
                file_props, finished_size, new = _inspect_file(
                    file_path,
                    db_data.get(str(file_path)),
                    dir_progress,
                    finished_size,
                    total_size,
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

    dup_list = [entry for entry in sorted(same_props.items()) if len(entry) > 1]

    return dup_list, files_props, new_files


def _inspect_file(
    file_path: Union_Path,
    existing_file_props: Optional[File_Props],
    dir_progress: str,
    finished_size: int,
    total_size: int,
    calculation_time: CalculationTime,
) -> tuple[Optional[File_Props], int, bool]:
    """
    Inspect all the files and get relevant properties

    Args:
        file_path           {Union_Path}          : Get file properties for file at path
        existing_file_props {Optional[File_Props]}: Existing data stored in the DB
        file_progress       {str}                 : File progress string
        finished_size       {int}                 : Total size of all finished files
        total_size          {int}                 : Total size of all files
        calculation_time    {CalculationTime}     : Data for processed calculation time

    Returns:
        {File_Props}: File properties of a file
        {int}       : Total size of all finished files, including this one
        {bool}      : Whether the file is new
    """
    stats = file_path.stat()
    size = stats.st_size
    last_modified = stats.st_mtime

    calculation_time.num_files_left -= 1

    if (
        existing_file_props is not None
        and existing_file_props.last_modified == last_modified
    ):
        finished_size += size
        clear_print(
            shrink_str(
                file_path.name,
                prefix=f"{progress_percent(finished_size, total_size)} {dir_progress}",
                postfix=time_remaining(calculation_time),
            ),
            end="",
        )
        return existing_file_props, finished_size, False

    num_chunks = ceil(size / _CHUNK_SIZE)

    md5 = md5_factory()
    sha1 = sha1_factory()

    start = time()

    try:
        with file_path.open("rb") as fp:
            for i in range(1, num_chunks + 1):
                chunk = fp.read(_CHUNK_SIZE)
                finished_size += len(chunk)
                clear_print(
                    shrink_str(
                        file_path.name,
                        prefix=f"{progress_percent(finished_size, total_size)} {dir_progress}",
                        postfix=f"[Chunk {progress_str(i, num_chunks)}] {time_remaining(calculation_time)}",
                    ),
                    end="",
                )
                md5.update(chunk)
                sha1.update(chunk)
    except PermissionError:
        return None, finished_size + file_path.stat().st_size, False
    else:
        calculation_time.num_processed_files += 1
        calculation_time.time_taken += time() - start
        return (
            File_Props(
                str(file_path),
                size,
                last_modified,
                md5.hexdigest(),
                sha1.hexdigest(),
            ),
            finished_size,
            True,
        )
