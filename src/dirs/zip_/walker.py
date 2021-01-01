"""
Module: Zip file walker

Public Functions:
    parse_zip
"""
from __future__ import annotations
from pathlib import Path
from typing import Generator

from .type_ import RootZipPath
from ..type_ import UnionPath
from ...config import WHITELIST


def check_zip(path: Path) -> bool:
    """
    Check if a file can be successfully opened as zip
    """
    try:
        with RootZipPath(path, True):
            pass
    except NotImplementedError:
        return False
    except FileNotFoundError:
        return False
    except PermissionError:
        return False
    else:
        return True


def parse_zip(path: Path) -> Generator[tuple[str, list[UnionPath]], None, None]:
    """
    Walk through a zip file

    Args:
        path (pathlib.Path): Path for the zip file

    Yields:
        (str)            : Path string
        (list[UnionPath]): List of paths in the folder
    """
    if path.name in WHITELIST.dirnames:
        return
    if str(path) in WHITELIST.dirpaths:
        return
    with RootZipPath(path) as zip_path:
        # Make linter happy
        files: list[UnionPath] = []
        files.append(zip_path)
        yield str(path), files
