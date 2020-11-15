"""
Module: Special types for annotations

Public Classes:
    Union_Path
"""
from __future__ import annotations
import pathlib
import zipfile
from typing import Union

Union_Path = Union[pathlib.Path, zipfile.Path]