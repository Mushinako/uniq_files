"""
Module: Directory walker
"""
from __future__ import annotations
from pathlib import Path
from typing import Generator, List, Tuple

from . import DIRECTORY_EXT
from ..config import WHITELIST
from ..utils.special_types import Union_Path


def _dir_walk_filtered(
    path: Path,
) -> Generator[Tuple[str, List[Union_Path]], None, None]:
    """
    Walk through directory and filter out whitelisted folders/files recursively

    Args:
        path {pathlib.Path}: Base path to be checked

    Yields:
        {str}             : Path string
        {list[Union_Path]}: List of paths in the folder
    """
    # Techinically {list[Path]}
    files: List[Union_Path] = []

    try:
        for subpath in path.iterdir():
            if subpath.is_symlink():
                continue
            elif subpath.is_dir():
                if subpath.name in WHITELIST.dirnames:
                    continue
                if subpath in WHITELIST.dirpaths:
                    continue
                yield from _dir_walk_filtered(subpath)
            elif (walk_gen := DIRECTORY_EXT.get(subpath.suffix, None)) is not None:
                if subpath.name in WHITELIST.dirnames:
                    continue
                if subpath in WHITELIST.dirpaths:
                    continue
                yield from walk_gen(subpath)
            else:
                if subpath.name in WHITELIST.filenames:
                    continue
                if subpath in WHITELIST.filepaths:
                    continue
                if any(
                    regex.fullmatch(str(subpath)) for regex in WHITELIST.fileregexes
                ):
                    continue
                files.append(subpath)
    except PermissionError:
        return

    yield str(path), files