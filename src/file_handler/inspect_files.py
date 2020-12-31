"""
Module: Inspect file properties

Public Functions:
    inspect_all_files
"""
from __future__ import annotations
from traceback import print_exc
from collections import defaultdict
from typing import Iterator

from .file_prop import FileProps
from ..dirs.type_ import UnionPath
from ..utils.print_funcs import clear_print
from ..utils.time_ import CalculationTime, Progress


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
                file_props_list, new_list = file_path.process(
                    db_data.get(str(file_path)),
                    dir_progress,
                    total_progress,
                    calculation_time,
                )
                new_files += new_list
                for path_str, props in file_props_list:
                    same_props[props.size, props.md5, props.sha1].append(path_str)
                    files_props.append(props)
    except KeyboardInterrupt:
        clear_print("Stopping...")
    except Exception:
        print_exc()

    dup_list = [entry for entry in sorted(same_props.items()) if len(entry) > 1]

    return dup_list, files_props, new_files
