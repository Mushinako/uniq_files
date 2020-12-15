"""
Module: Zip file walker

Public Functions:
    parse_zip
"""
from __future__ import annotations
from pathlib import Path
from typing import Generator

from ..config import WHITELIST
from ..types_.dir_types import Zip_Path


def parse_zip(path: Path) -> Generator[tuple[str, list[Zip_Path]], None, None]:
    """
    Walk through a zip file

    Args:
        path {pathlib.Path}: Path for the zip file

    Yields:
        {str}               : Path string
        {list[zipfile.Path]}: List of paths in the folder
    """
    zip_path = Zip_Path(path)
    yield from _zip_walk_filtered(zip_path)


def _zip_walk_filtered(
    path: Zip_Path,
) -> Generator[tuple[str, list[Zip_Path]], None, None]:
    """
    Walk through zip and filter out whitelisted folders/files recursively

    Args:
        path {zipfile.Path}: Base path to be checked

    Yields:
        {str}               : Path string
        {list[zipfile.Path]}: List of paths
    """
    files: list[Zip_Path] = []

    try:
        for subpath in path.iterdir():
            if subpath.is_dir():
                if subpath.name in WHITELIST.dirnames:
                    continue
                if subpath in WHITELIST.dirpaths:
                    continue
                yield from _zip_walk_filtered(subpath)
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
