"""
Module: Special directory types

Public Classes:
    Zip_Path
    Union_Path
    Union_Path_Types
"""
from __future__ import annotations
import re
import pathlib
import zipfile
from datetime import datetime
from typing import Union


class ZipPath(zipfile.Path):
    """
    Similar to zipfile.Path, but implements a `stat().st_size` and `stat().st_mtime`

    Public Methods:
        stat
    """

    _ZIP_PATH_REGEX = re.compile(r"(?<=.zip)/")

    # Technically `zipfile.FastLookup` but no matter
    root: zipfile.ZipFile
    at: str

    def __enter__(self) -> ZipPath:
        return self

    def __exit__(self, *_) -> None:
        self.root.close()

    def __eq__(self, o: ZipPath) -> bool:
        return str(self) == str(o)

    def __lt__(self, o: ZipPath) -> bool:
        return str(self) < str(o)

    def _next(self, at: str) -> ZipPath:
        return self.__class__(self.root, at)

    def stat(self) -> _Zip_Stat_Result:
        """
        Get stats for the file at this path
        """
        zip_info_obj = self.root.getinfo(self.at)
        return _Zip_Stat_Result(zip_info_obj)

    @classmethod
    def from_zip_path(cls, path: str) -> ZipPath:
        """
        Get Zip_Path object from full compressed file path
        """
        root, *rest = ZipPath._ZIP_PATH_REGEX.split(path)
        if not root.endswith(".zip"):
            raise ValueError(f"Not a valid compressed file path: {path}")
        at = "/".join(rest)
        obj = cls(root, at)
        obj.root.close()
        return obj


Union_Path = Union[pathlib.Path, ZipPath]


class _Zip_Stat_Result:
    """
    Custom class emulating some functionalities of `os.stat_result` for zip file

    Properties:
        st_size  {int}  : File size
        st_mtime {float}: Last modified time
    """

    def __init__(self, zip_info_obj: zipfile.ZipInfo) -> None:
        self.st_size = zip_info_obj.file_size
        date_time = (
            zip_info_obj.date_time[0],
            month if (month := zip_info_obj.date_time[1]) else 1,
            day if (day := zip_info_obj.date_time[2]) else 1,
            zip_info_obj.date_time[3],
            zip_info_obj.date_time[4],
            zip_info_obj.date_time[5],
        )
        self.st_mtime = datetime(*date_time).timestamp()
