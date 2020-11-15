"""
"""
from math import ceil
from hashlib import md5 as md5_, sha1 as sha1_
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional, Tuple

from .utils import progress_str, progress_percent, process_str_len

CHUNK_SIZE = 1 << 26  # 64 MiB


@dataclass
class File_Data:
    path: Path
    size: int
    last_modified: float
    md5: str
    sha1: str


def _get_file_properties(
    path: Path,
    file_progress: str,
    existing_file_data: Optional[File_Data],
    finished_size: int,
    total_size: int,
) -> Tuple[File_Data, int]:
    """"""
    stat = path.stat()
    last_modified = stat.st_mtime
    size = path.stat().st_size
    if (
        existing_file_data is not None
        and existing_file_data.last_modified == last_modified
    ):
        finished_size += size
        print(
            process_str_len(
                path.name,
                prefix=progress_percent(finished_size, total_size) + file_progress,
            ),
            end="",
        )
        return existing_file_data, finished_size

    md5 = md5_()
    sha1 = sha1_()

    num_chunks = ceil(size / CHUNK_SIZE)

    with path.open("rb") as fp:
        for i in range(1, num_chunks + 1):
            chunk = fp.read(CHUNK_SIZE)
            finished_size += len(chunk)
            print(
                process_str_len(
                    path.name,
                    prefix=progress_percent(finished_size, total_size) + file_progress,
                    postfix=" [Chunk " + progress_str(i, num_chunks) + "]",
                ),
                end="",
            )
            md5.update(chunk)
            sha1.update(chunk)

    return (
        File_Data(path, size, last_modified, md5.hexdigest(), sha1.hexdigest()),
        finished_size,
    )


def check_files(
    walker: Generator[Tuple[str, Path], None, None],
    files_data: Dict[Path, File_Data],
    total_size: int,
) -> Tuple[List[Dict], List[File_Data]]:
    """"""
    same_props: Dict[Tuple[int, str, str], List[str]] = defaultdict(lambda: [])
    all_files: List[File_Data] = []

    finished_size = 0

    print()

    try:
        for file_progress, path in walker:
            file_data, finished_size = _get_file_properties(
                path,
                file_progress,
                files_data.get(path, None),
                finished_size,
                total_size,
            )
            same_props[file_data.size, file_data.md5, file_data.sha1].append(str(path))
            all_files.append(file_data)
    except KeyboardInterrupt:
        print("\r\x1b[KStopping...")

    duplication_list: List[Tuple[int, str, str, List[str]]] = [
        (*properties, paths)
        for properties, paths in same_props.items()
        if len(paths) > 1
    ]

    output_json_list: List[Dict] = [
        {
            "properties": {
                "size": size,
                "hashes": {
                    "md5": md5,
                    "sha1": sha1,
                },
            },
            "paths": paths,
        }
        for size, md5, sha1, paths in duplication_list
    ]

    return output_json_list, all_files
