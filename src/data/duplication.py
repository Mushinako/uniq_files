"""
Module: File duplication

Public Classes:
    Duplication: Dataclass containing duplication entries
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Duplication:
    """
    Dataclass containing duplication entries

    Args:
        size  (int)      : File size
        md5   (str)      : MD5 hash
        sha1  (str)      : SHA-1 hash
        paths (list[str]): List of path strings with such data

    Public Attributes:
        size  (int)      : File size
        md5   (str)      : MD5 hash
        sha1  (str)      : SHA-1 hash
        paths (list[str]): List of path strings with such data

    Public Method:
        to_json_dict: Export duplication data to json-formatted dict
    """

    size: int
    md5: str
    sha1: str
    paths: list[str]

    def __lt__(self, other: Duplication) -> bool:
        return (self.size, self.md5, self.sha1) < (other.size, other.md5, other.sha1)

    def to_json_dict(self):
        return {
            "properties": {
                "size": self.size,
                "hashes": {"md5": self.md5, "sha1": self.sha1},
            },
            "paths": self.paths,
        }
