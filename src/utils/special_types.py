"""
Module: Special types for annotations

Public Classes:
    Union_Path
"""
from __future__ import annotations
import zipfile


class Zip_Path(zipfile.Path):
    """
    Similar to zipfile.Path, but implements a `stat().st_size` and `stat().st_mtime`
    """

    # Technically `zipfile.FastLookup` but no matter
    root: zipfile.ZipFile

    def _next(self, at: str) -> Zip_Path:
        return Zip_Path(self.root, at)
