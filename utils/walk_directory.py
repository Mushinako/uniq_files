"""
"""
import zipfile
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, Dict, Generator, List, Tuple, Union

from .config import WHITELIST
from .type_parser import DIRECTORY_EXT
from .utils import progress_str, process_str_len


@dataclass
class File_Property:
    """"""

    md5_: str
    sha1_: str
    sha512_: str
    size: int

    def __hash__(self) -> int:
        return hash((self.md5_, self.sha1_, self.sha512_, self.size))


def _os_walk_filtered(
    path: Path,
) -> Generator[Tuple[str, Union[List[Path], List[zipfile.Path]]], None, None]:
    """"""
    dirs: List[Path] = []
    dirfiles: Dict[
        Path, Callable[[Path], Generator[Tuple[str, List[zipfile.Path]], None, None]]
    ] = {}
    nondirs: List[Path] = []

    try:
        for subpath in path.resolve().iterdir():
            if subpath.is_dir():
                if subpath.is_symlink():
                    continue
                if subpath.name in WHITELIST.dirnames:
                    continue
                if subpath in WHITELIST.dirpaths:
                    continue
                dirs.append(subpath)
            elif subpath.suffix in DIRECTORY_EXT:
                if subpath.is_symlink():
                    continue
                if subpath.name in WHITELIST.dirnames:
                    continue
                if subpath in WHITELIST.dirpaths:
                    continue
                dirfiles[subpath] = DIRECTORY_EXT[subpath.suffix]
            else:
                if subpath.name in WHITELIST.filenames:
                    continue
                if subpath in WHITELIST.filepaths:
                    continue
                if any(
                    regex.fullmatch(str(subpath)) for regex in WHITELIST.fileregexes
                ):
                    continue
                nondirs.append(subpath)
    except PermissionError:
        return

    yield str(path), nondirs

    for subdir in dirs:
        yield from _os_walk_filtered(subdir)


def iter_walk(
    base_path: Path,
) -> Generator[Tuple[str, Union[Path, zipfile.Path]], None, None]:
    """
    Iterate through all files that are descendants of `base_path`, recursively
    """
    for dir_path, file_paths in _os_walk_filtered(base_path):
        print(process_str_len(dir_path, prefix="Checking directory "), end="\r")
        num_files = len(file_paths)
        for file_id, file_path in enumerate(file_paths):
            yield "[File " + progress_str(file_id + 1, num_files) + "] ", file_path


def iter_walk_size(base_path: Path) -> int:
    """"""
    total_sum = 0
    for dir_path, file_paths in _os_walk_filtered(base_path):
        print(process_str_len(dir_path), end="\r")
        total_sum += sum(path.stat().st_size for path in file_paths)
    return total_sum
