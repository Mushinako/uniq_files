"""
Module: Special file properties stuff

Public Classes:
    FileProps
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FileProps:
    """
    File properties

    Properties:
        path          (str)  : Path of the file
        size          (int)  : File size
        last_modified (float): Last modified timestamp
        md5           (str)  : MD5 hash
        sha1          (str)  : SHA-1 hash
    """

    path: str
    size: int
    last_modified: float
    md5: str
    sha1: str
