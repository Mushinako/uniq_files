"""
"""
from pathlib import Path
from dataclasses import dataclass
from typing import Generator, List, Tuple

from .config import WHITELIST
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


def _os_walk_filtered(path: Path) -> Generator[Tuple[Path, List[Path]], None, None]:
    """"""
    dirs: List[Path] = []
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

    yield path, nondirs

    for subdir in dirs:
        yield from _os_walk_filtered(subdir)


def iter_walk(base_path: Path) -> Generator[Tuple[str, Path], None, None]:
    """
    Iterate through all files that are descendants of `base_path`, recursively
    """
    for dir_path, file_paths in _os_walk_filtered(base_path):
        print(process_str_len(dir_path, prefix="\r\x1b[KChecking directory "))
        num_files = len(file_paths)
        for file_id, file_path in enumerate(file_paths):
            yield progress_str(file_id + 1, num_files), file_path
