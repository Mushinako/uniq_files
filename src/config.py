"""
Module: Configurations

Public Constants:
    WHITELIST {_Whitelist}: All the whitelists
"""
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Pattern, Set


# Config to be edited
_WHITELIST_DIRNAMES: List[str] = [
    ".git",
    ".vscode",
    "site-packages",
    "__pycache__",
    "node_modules",
]
_WHITELIST_DIRPATHS: List[str] = []
_WHITELIST_FILENAMES: List[str] = [".gitignore", "__init__.py"]
_WHITELIST_FILEPATHS: List[str] = []
_WHITELIST_FILEREGEXES: List[str] = []


@dataclass
class _Whitelist:
    """"""

    dirnames: Set[str]
    dirpaths: Set[Path]
    filenames: Set[str]
    filepaths: Set[Path]
    fileregexes: List[Pattern[str]]


WHITELIST = _Whitelist(
    set(_WHITELIST_DIRNAMES),
    set(Path(path).resolve() for path in _WHITELIST_DIRPATHS),
    set(_WHITELIST_FILENAMES),
    set(Path(path).resolve() for path in _WHITELIST_FILEPATHS),
    [re.compile(regex) for regex in _WHITELIST_FILEREGEXES],
)