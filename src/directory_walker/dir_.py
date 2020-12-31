"""
Module: Directory walker

Public Functions:
    parse_dir
"""
from __future__ import annotations
from pathlib import Path
from typing import Generator

from . import DIRECTORY_EXT
from ..config import WHITELIST
from ..types_.dir_types import Union_Path


def parse_dir(path: Path) -> Generator[tuple[str, list[Union_Path]], None, None]:
    """
    Walk through directory

    Args:
        path {pathlib.Path}: Base path to be checked

    Yields:
        {str}             : Path string
        {list[Union_Path]}: List of paths in the folder
    """
    yield from _dir_walk_filtered(path)


def _dir_walk_filtered(
    path: Path,
) -> Generator[tuple[str, list[Union_Path]], None, None]:
    """
    Walk through directory and filter out whitelisted folders/files recursively

    Args:
        path {pathlib.Path}: Base path to be checked

    Yields:
        {str}             : Path string
        {list[Union_Path]}: List of paths in the folder
    """
    # Techinically {list[Path]}
    files: list[Union_Path] = []

    try:
        for subpath in sorted(path.iterdir()):
            if subpath.is_symlink():
                continue
            if subpath.is_dir():
                if subpath.name in WHITELIST.dirnames:
                    continue
                if subpath in WHITELIST.dirpaths:
                    continue
                yield from _dir_walk_filtered(subpath)
                continue
            if (config := DIRECTORY_EXT.get(subpath.suffix, None)) is not None:
                test, walk_gen = config
                if test(subpath):
                    if subpath.name in WHITELIST.dirnames:
                        continue
                    if subpath in WHITELIST.dirpaths:
                        continue
                    yield from walk_gen(subpath)
                    continue
            if subpath.name in WHITELIST.filenames:
                continue
            if subpath in WHITELIST.filepaths:
                continue
            if any(regex.fullmatch(str(subpath)) for regex in WHITELIST.fileregexes):
                continue
            files.append(subpath)
            continue
    except PermissionError:
        return

    yield str(path), files
