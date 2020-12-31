"""
Module: Zip file walker

Public Functions:
    parse_zip
"""
from __future__ import annotations
from pathlib import Path
from typing import Generator

from ..config import WHITELIST
from ..types_.dir_types import Union_Path, ZipPath


def check_zip(path: Path) -> bool:
    """
    Check if a file can be successfully opened as zip
    """
    try:
        with ZipPath(path):
            pass
    except NotImplementedError:
        return False
    except FileNotFoundError:
        return False
    except PermissionError:
        return False
    else:
        return True


def parse_zip(path: Path) -> Generator[tuple[str, list[Union_Path]], None, None]:
    """
    Walk through a zip file

    Args:
        path {pathlib.Path}: Path for the zip file

    Yields:
        {str}             : Path string
        {list[Union_Path]}: List of paths in the folder
    """
    with ZipPath(path) as zip_path:
        yield from _zip_walk_filtered(zip_path)


def _zip_walk_filtered(
    path: ZipPath,
) -> Generator[tuple[str, list[Union_Path]], None, None]:
    """
    Walk through zip and filter out whitelisted folders/files recursively

    Args:
        path {ZipPath}: Base path to be checked

    Yields:
        {str}             : Path string
        {list[Union_Path]}: List of paths
    """
    # Techinically {list[ZipPath]}
    files: list[Union_Path] = []

    try:
        for subpath in sorted(path.iterdir()):
            if subpath.is_dir():
                if subpath.name in WHITELIST.dirnames:
                    continue
                if str(subpath) in WHITELIST.dirpaths:
                    continue
                yield from _zip_walk_filtered(subpath)
            else:
                if subpath.name in WHITELIST.filenames:
                    continue
                if (subpath_str := str(subpath)) in WHITELIST.filepaths:
                    continue
                if any(regex.fullmatch(subpath_str) for regex in WHITELIST.fileregexes):
                    continue
                files.append(subpath)
    except PermissionError:
        return
    else:
        yield str(path), files
