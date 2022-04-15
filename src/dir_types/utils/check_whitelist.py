"""
Module: Check if a directory/file is in the whitelist

Public Functions:
    check_dir : Check if a directory is in the whitelist
    check_file: Check if a file is in the whitelist
"""

from __future__ import annotations

from src.config import WHITELIST
from src.dir_types.common import BasePath


def check_dir(path: BasePath) -> bool:
    """
    Check if a directory is in the whitelist

    Args:
        path (UnionPath): The path to be checked, assuming it's a directory

    Returns:
        (bool): Whether the path should be included; i.e., not in the whitelist
    """
    return path.name not in WHITELIST.dirnames and str(path) not in WHITELIST.dirpaths


def check_file(path: BasePath) -> bool:
    """
    Check if a file is in the whitelist

    Args:
        path (UnionPath): The path to be checked, assuming it's a file

    Returns:
        (bool): Whether the path should be included; i.e., not in the whitelist
    """
    return (
        path.name not in WHITELIST.filenames
        and (subpath_str := str(path)) not in WHITELIST.filepaths
        and not any(regex.fullmatch(subpath_str) for regex in WHITELIST.fileregexes)
    )
