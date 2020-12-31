from __future__ import annotations
import pathlib
import zipfile
from typing import Iterator, Union

class Zip_Path(zipfile.Path):
    def __enter__(self) -> Zip_Path: ...
    def __exit__(self, *_) -> None: ...
    def __eq__(self, o: Zip_Path) -> bool: ...
    def __lt__(self, o: Zip_Path) -> bool: ...
    def iterdir(self) -> Iterator[Zip_Path]: ...
    def joinpath(self, add: zipfile.StrPath) -> Zip_Path: ...  # undocumented
    def __truediv__(self, add: zipfile.StrPath) -> Zip_Path: ...
    def stat(self) -> _Zip_Stat_Result: ...
    @classmethod
    def from_zip_path(cls, path: str) -> Zip_Path: ...

Union_Path = Union[pathlib.Path, Zip_Path]
Union_Path_Types = Union[type[pathlib.Path], type[Zip_Path]]

class _Zip_Stat_Result:
    st_size: int
    st_mtime: float
    def __init__(self, zip_info_obj: zipfile.ZipInfo) -> None: ...
