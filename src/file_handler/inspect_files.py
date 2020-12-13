"""
Module: Inspect file properties

Public Functions:
    inspect_all_files
"""
from __future__ import annotations
from math import ceil
from collections import defaultdict
from hashlib import md5 as md5_factory, sha1 as sha1_factory
from typing import Dict, Iterator, List, Optional, Tuple

from ..utils.print_funcs import clear_print, progress_percent, progress_str, shrink_str
from ..types_.dir_types import Union_Path
from ..types_.file_prop import File_Props, class_2_type

_CHUNK_SIZE = 1 << 26  # 64 MiB


def inspect_all_files(
    files_gen: Iterator[Tuple[str, List[Union_Path]]],
    db_data: Dict[Union_Path, File_Props],
    total_size: int,
) -> Tuple[
    List[Dict[str, Dict[str, int | Dict[str, str]] | List[str]]],
    List[File_Props],
]:
    """
    Inspect all the files and get relevant properties

    Args:
        files_gen  {Iterator[tuple[str, list[Union_Path]]]}:
            Iterator that generates (dir_path, files) pairs
        db_data    {dict[Union_Path, File_Props]}: Existing path-file property mapping
        total_size {int}                         : Total size of all files

    Returns:
        {list[dict[str, dict[str, int | dict[str, str]] | list[str]]]}:
            All duplications
        {list[File_Props]}: All file properties
    """
    same_props: Dict[Tuple[int, str, str], List[str]] = defaultdict(lambda: [])
    files_props: List[File_Props] = []
    finished_size = 0

    try:
        for dir_path, file_paths in files_gen:
            clear_print(f"Walking {dir_path}...")
            num_files = len(file_paths)
            for i, file_path in enumerate(file_paths):
                dir_progress = f"[File {progress_str(i, num_files)}]"
                file_props, finished_size = _inspect_file(
                    file_path,
                    db_data.get(file_path),
                    dir_progress,
                    finished_size,
                    total_size,
                )
                if file_props is None:
                    continue
                same_props[file_props.size, file_props.md5, file_props.sha1].append(
                    str(file_path)
                )
                files_props.append(file_props)
    except KeyboardInterrupt:
        clear_print("Stopping...")

    # Get duplications
    duplication_list = [
        {
            "properties": {
                "size": size,
                "hashes": {
                    "md5": md5,
                    "sha1": sha1,
                },
            },
            "paths": file_paths,
        }
        for (size, md5, sha1), file_paths in sorted(same_props.items())
        if len(file_paths) > 1
    ]

    return duplication_list, files_props


def _inspect_file(
    file_path: Union_Path,
    existing_file_props: Optional[File_Props],
    dir_progress: str,
    finished_size: int,
    total_size: int,
) -> Tuple[Optional[File_Props], int]:
    """
    Inspect all the files and get relevant properties

    Args:
        file_path           {Union_Path}          : Get file properties for file at path
        existing_file_props {Optional[File_Props]}: Existing data stored in the DB
        file_progress       {str}                 : File progress string
        finished_size       {int}                 : Total size of all finished files
        total_size          {int}                 : Total size of all files

    Returns:
        {File_Props}: File properties of a file
        {int}       : Total size of all finished files, including this one
    """
    stats = file_path.stat()
    size = stats.st_size
    last_modified = stats.st_mtime

    if (
        existing_file_props is not None
        and existing_file_props.last_modified == last_modified
    ):
        finished_size += size
        clear_print(
            shrink_str(
                file_path.name,
                prefix=f"{progress_percent(finished_size, total_size)} {dir_progress}",
            ),
            end="",
        )
        return existing_file_props, finished_size

    num_chunks = ceil(size / _CHUNK_SIZE)

    md5 = md5_factory()
    sha1 = sha1_factory()

    try:
        with file_path.open("rb") as fp:
            for i in range(1, num_chunks + 1):
                chunk = fp.read(_CHUNK_SIZE)
                finished_size += len(chunk)
                clear_print(
                    shrink_str(
                        file_path.name,
                        prefix=f"{progress_percent(finished_size, total_size)} {dir_progress}",
                        postfix=f"[Chunk {progress_str(i, num_chunks)}]",
                    ),
                    end="",
                )
                md5.update(chunk)
                sha1.update(chunk)
    except PermissionError:
        return (None, finished_size + file_path.stat().st_size)
    else:
        return (
            File_Props(
                file_path,
                class_2_type(type(file_path)),
                size,
                last_modified,
                md5.hexdigest(),
                sha1.hexdigest(),
            ),
            finished_size,
        )
