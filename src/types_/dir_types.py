"""
Module: Special directory types

Public Classes:
    Zip_Path
    Union_Path
    Union_Path_Types
"""
from __future__ import annotations
import pathlib
import zipfile
from datetime import datetime
from typing import Union


class Zip_Path(zipfile.Path):
    """
    Similar to zipfile.Path, but implements a `stat().st_size` and `stat().st_mtime`

    Public Methods:
        stat
    """

    # Technically `zipfile.FastLookup` but no matter
    root: zipfile.ZipFile
    at: str

    def _next(self, at: str) -> Zip_Path:
        return Zip_Path(self.root, at)

    def stat(self) -> _Zip_Stat_Result:
        """
        Get stats for the file at this path
        """
        zip_info_obj = self.root.getinfo(self.at)
        return _Zip_Stat_Result(zip_info_obj)


Union_Path = Union[pathlib.Path, Zip_Path]
Union_Path_Types = Union[type[pathlib.Path], type[Zip_Path]]


class _Zip_Stat_Result:
    """
    Custom class emulating some functionalities of `os.stat_result` for zip file

    Properties:
        st_size  {int}  : File size
        st_mtime {float}: Last modified time
    """

    def __init__(self, zip_info_obj: zipfile.ZipInfo) -> None:
        self.st_size = zip_info_obj.file_size
        self.st_mtime = datetime(*zip_info_obj.date_time).timestamp()
