from __future__ import annotations
import pathlib
import zipfile
from typing import Iterator, Union

class Zip_Path(zipfile.Path):
    def iterdir(self) -> Iterator[Zip_Path]: ...
    def joinpath(self, add: zipfile.StrPath) -> Zip_Path: ...  # undocumented
    def __truediv__(self, add: zipfile.StrPath) -> Zip_Path: ...
    def stat(self) -> _Zip_Stat_Result: ...

Union_Path = Union[pathlib.Path, Zip_Path]

class _Zip_Stat_Result:
    st_size: int
    st_mtime: float
    def __init__(self, zip_info_obj: zipfile.ZipInfo) -> None: ...
