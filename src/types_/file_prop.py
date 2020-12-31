"""
Module: Special file properties stuff

Public Classes:
    Path_Type
    File_Props

Public Functions:
    class_2_type

Public Constants:
    PATH_CLASS_MAP
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class File_Props:
    """
    File properties

    Properties:
        path {str}: Path of the file
        size {int}
        last_modified {float}
        md5 {str}
        sha1 {str}
    """

    path: str
    size: int
    last_modified: float
    md5: str
    sha1: str
