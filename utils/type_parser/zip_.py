import zipfile
from pathlib import Path
from typing import Generator, List, Tuple

from ..config import WHITELIST


def _zip_walk_filtered(path: zipfile.Path)->Generator[Tuple[str, List[Path]], None, None]:
    """"""
    dirs: List[Path] = []
    nondirs: List[Path] = []

    try:
        for subpath in path.iterdir():
            if subpath.is_dir():
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


def parse_zip(path: Path) -> Generator[Tuple[str, List[Path]], None, None]:
    """"""
    zip_path = zipfile.Path(path, "r")
    yield from _zip_walk_filtered(zip_path)
