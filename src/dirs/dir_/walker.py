"""
Module: Directory walker

Public Functions:
    parse_dir
"""
from __future__ import annotations
from pathlib import Path
from typing import Generator

from .type_ import DirPath
from .. import DIRECTORY_EXT
from ..type_ import UnionPath
from ...config import WHITELIST


def parse_dir(path: Path) -> Generator[tuple[str, list[UnionPath]], None, None]:
    """
    Walk through directory

    Args:
        path (pathlib.Path): Base path to be checked

    Yields:
        (str)            : Path string
        (list[UnionPath]): List of paths in the folder
    """
    yield from _dir_walk_filtered(path)


def _dir_walk_filtered(
    path: Path,
) -> Generator[tuple[str, list[UnionPath]], None, None]:
    """
    Walk through directory and filter out whitelisted folders/files recursively

    Args:
        path (pathlib.Path): Base path to be checked

    Yields:
        (str)            : Path string
        (list[UnionPath]): List of paths in the folder
    """
    # Technically list[DirPath]
    files: list[UnionPath] = []

    try:
        for subpath in sorted(path.iterdir()):
            if subpath.is_symlink():
                continue
            if subpath.is_dir():
                if subpath.name in WHITELIST.dirnames:
                    continue
                if str(subpath) in WHITELIST.dirpaths:
                    continue
                yield from _dir_walk_filtered(subpath)
                continue
            if (config := DIRECTORY_EXT.get(subpath.suffix, None)) is not None:
                test, walk_gen = config
                if test(subpath):
                    if subpath.name in WHITELIST.dirnames:
                        continue
                    if str(subpath) in WHITELIST.dirpaths:
                        continue
                    yield from walk_gen(subpath)
                    continue
            if subpath.name in WHITELIST.filenames:
                continue
            if (subpath_str := str(subpath)) in WHITELIST.filepaths:
                continue
            if any(regex.fullmatch(subpath_str) for regex in WHITELIST.fileregexes):
                continue
            files.append(DirPath(subpath))
            continue
    except PermissionError:
        return

    yield str(path), files
