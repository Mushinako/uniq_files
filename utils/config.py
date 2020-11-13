"""
"""
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Pattern

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

    dirnames: List[str]
    dirpaths: List[Path]
    filenames: List[str]
    filepaths: List[Path]
    fileregexes: List[Pattern[str]]


WHITELIST = _Whitelist(
    _WHITELIST_DIRNAMES,
    [Path(path).resolve() for path in _WHITELIST_DIRPATHS],
    _WHITELIST_FILENAMES,
    [Path(path).resolve() for path in _WHITELIST_FILEPATHS],
    [re.compile(regex) for regex in _WHITELIST_FILEREGEXES],
)
