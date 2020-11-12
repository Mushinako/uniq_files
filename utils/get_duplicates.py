from math import ceil
from shutil import get_terminal_size
from pathlib import Path
from hashlib import md5, sha1, sha512
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Generator, List, Tuple

from utils.utils import CONFIG, progress_str

CHUNK_SIZE = 1 << 24  # 16 MiB
WHITELIST = CONFIG.whitelist


@dataclass
class File_Property:
    """"""

    md5_: str
    sha1_: str
    sha512_: str
    size: int

    def __hash__(self) -> int:
        return hash((self.md5_, self.sha1_, self.sha512_, self.size))


def os_walk_filtered(path: Path) -> Generator[Tuple[Path, List[Path]], None, None]:
    """"""
    dirs: List[Path] = []
    nondirs: List[Path] = []

    try:
        for subpath in path.resolve().iterdir():
            if subpath.is_dir():
                if subpath.is_symlink():
                    continue
                if subpath.name in WHITELIST.dir_names:
                    continue
                if str(subpath) in WHITELIST.dir_paths:
                    continue
                dirs.append(subpath)
            else:
                if subpath.name in WHITELIST.file_names:
                    continue
                subpath_str = str(subpath)
                if subpath_str in WHITELIST.file_paths:
                    continue
                if any(r.fullmatch(subpath_str) for r in WHITELIST.file_regexes):
                    continue
                nondirs.append(subpath)
    except PermissionError:
        return

    yield path, nondirs

    for dirpath in dirs:
        yield from os_walk_filtered(dirpath)


def iter_walk(base_path: Path) -> Generator[Tuple[int, int, Path], None, None]:
    """
    Iterate through all files that are descendants of `base_path`, recursively
    """
    for dir_path, file_paths in os_walk_filtered(base_path):
        print(f"\r\x1b[KChecking directory {dir_path}")
        num_files = len(file_paths)
        for file_id, file_path in enumerate(file_paths):
            yield file_id + 1, num_files, file_path


def get_file_properties(path: Path, id_: int, count: int) -> File_Property:
    """
    Get file properties, to be used as unique key for each file

    Args:
        path {Path} - The path of the file to be checked
    """
    md5_ = md5()
    sha1_ = sha1()
    sha512_ = sha512()
    size = path.stat().st_size

    num_of_chunks = ceil(size / CHUNK_SIZE)

    file_counter = f"[File:{progress_str(id_, count)}]"

    with path.open("rb") as fp:
        for i in range(1, num_of_chunks + 1):
            chunk_counter = f"[Chunk:{progress_str(i, num_of_chunks)}]"
            print(
                f"\r\x1b[K{file_counter} {path.name[:get_terminal_size().columns-4-len(file_counter)-len(chunk_counter)]} {chunk_counter}",
                end="",
                flush=True,
            )
            chunk = fp.read(CHUNK_SIZE)
            md5_.update(chunk)
            sha1_.update(chunk)
            sha512_.update(chunk)

    file_properties = File_Property(
        md5_.hexdigest(),
        sha1_.hexdigest(),
        sha512_.hexdigest(),
        size,
    )
    return file_properties


def get_duplicates(base_path) -> List[Dict]:
    """
    Get duplication info under a base path
    """

    all_files: defaultdict[File_Property, List[str]] = defaultdict(list)
    print()
    for id_, count, path in iter_walk(base_path):
        properties = get_file_properties(path, id_, count)
        all_files[properties].append(str(path))
    print("\r\x1b[K")
    print()

    duplicates_list: List[Dict] = []
    for properties, paths in all_files.items():
        if len(paths) == 1:
            continue
        paths.sort()
        properties_dict = {
            "size": properties.size,
            "hashes": {
                "md5": properties.md5_,
                "sha1": properties.sha1_,
                "sha512": properties.sha512_,
            },
        }
        duplication_entry = {
            "properties": properties_dict,
            "paths": paths,
        }
        duplicates_list.append(duplication_entry)

    duplicates_list.sort(key=lambda d: d["properties"]["size"])
    return duplicates_list


def write_duplicates() -> None:
    """"""