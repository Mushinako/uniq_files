"""
"""
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Pattern, Set

# Config to be edited
_WHITELIST_DIRNAMES = [
    ".git",
    ".vscode",
    "site-packages",
    "__pycache__",
    "node_modules",
]
_WHITELIST_DIRPATHS = []
_WHITELIST_FILENAMES = [".gitignore", "__init__.py"]
_WHITELIST_FILEPATHS = []
_WHITELIST_FILEREGEXES = []


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
