"""
"""
from math import ceil
from hashlib import md5 as md5_, sha1 as sha1_
from pathlib import Path
from dataclasses import dataclass
from typing import Generator, Tuple

from .utils import progress_str, process_str_len

CHUNK_SIZE = 1 << 26  # 64 MiB


@dataclass
class File_Data:
    path: Path
    size: int
    last_modified: int
    md5: str
    sha1: str


def get_file_properties(path: Path, file_progress: str) -> File_Data:
    """"""
    md5 = md5_()
    sha1 = sha1_()
    stat = path.stat()
    size = stat.st_size

    num_chunks = ceil(size / CHUNK_SIZE)

    with path.open("wb") as fp:
        for i in range(1, num_chunks + 1):
            print(
                process_str_len(
                    path.name,
                    prefix=file_progress,
                    postfix=" [Chunk " + progress_str(i, num_chunks) + "]",
                ),
                end="",
            )
            chunk = fp.read(CHUNK_SIZE)
            md5.update(chunk)
            sha1.update(chunk)

    return File_Data(path, size, stat.st_mtime, md5, sha1)


def check_files(walker: Generator[Tuple[str, Path], None, None]) -> None:
    """"""
    for file_progress, path in walker:
        pass
