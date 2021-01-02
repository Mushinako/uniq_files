"""
Module: File statistics

Public Classes:
    FileStat: Dataclass containing file statistics

Public Types:
    DatabaseRow: A row of database data
    IdStats    : Identifying stats of a file (size, MD5 hash, and SHA-1 hash)
"""

from __future__ import annotations

from dataclasses import dataclass

DatabaseRow = tuple[str, str, str, str, str]
IdStat = tuple[int, str, str]


@dataclass
class FileStat:
    """
    Dataclass containing file statistics

    Args:
        path  (str)  : Path of the file
        size  (int)  : File size
        mtime (float): Last modified timestamp
        md5   (str)  : MD5 hash
        sha1  (str)  : SHA-1 hash

    Public Attributes:
        path  (str)  : Path of the file
        size  (int)  : File size
        mtime (float): Last modified timestamp
        md5   (str)  : MD5 hash
        sha1  (str)  : SHA-1 hash

    Public Methods:
        to_db_row:
            Export to database row. Namely, a collection of strings
        from_db_row (classmethod):
            Construct object from database row
    """

    path: str
    size: int
    mtime: float
    md5: str
    sha1: str

    def to_db_row(self) -> DatabaseRow:
        """
        Export to database row. Namely, a collection of strings

        Returns:
            (DatabaseRow): A row of database data corresponding to this object
        """
        return self.path, str(self.size), str(self.mtime), self.md5, self.sha1

    def to_id_stat(self) -> IdStat:
        """
        Export identifying information

        Returns:
            (IdStat): Identifying information (size, MD5 hash, SHA-1 hash)
        """
        return self.size, self.md5, self.sha1

    @classmethod
    def from_db_row(cls, db_row: DatabaseRow) -> FileStat:
        """
        Construct object from database row

        Args:
            db_row (DatabaseRow): A row of database data

        Returns:
            (FileStat): Corresponding `FileStat` object
        """
        path, size, mtime, md5, sha1 = db_row
        return cls(path, int(size), float(mtime), md5, sha1)
