"""
Module: Configurations

Public Constants:
    WHITELIST {_Whitelist}: All the whitelists
"""
import re
from dataclasses import dataclass


# Config to be edited
_WHITELIST_DIRNAMES: list[str] = [
    ".git",
    ".vscode",
    "site-packages",
    "__pycache__",
    "node_modules",
]
_WHITELIST_DIRPATHS: list[str] = []
_WHITELIST_FILENAMES: list[str] = [".gitignore", "__init__.py"]
_WHITELIST_FILEPATHS: list[str] = []
_WHITELIST_FILEREGEXES: list[str] = []


@dataclass
class _Whitelist:
    """"""

    dirnames: set[str]
    dirpaths: set[str]
    filenames: set[str]
    filepaths: set[str]
    fileregexes: list[re.Pattern[str]]


WHITELIST = _Whitelist(
    set(_WHITELIST_DIRNAMES),
    set(_WHITELIST_DIRPATHS),
    set(_WHITELIST_FILENAMES),
    set(_WHITELIST_FILEPATHS),
    [re.compile(regex) for regex in _WHITELIST_FILEREGEXES],
)
