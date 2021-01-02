"""
Module: Reading from and writing to sqlite3 database

Public Classes:
    DB: Database I/O
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from ..data.file_stat import FileStat, DatabaseRow
from ..utils.print_ import clear_print


class Db:
    """
    Database I/O

    Args:
        path (pathlib.Path): Database file path

    Public Attributes:
        path (pathlib.Path): Database file path

    Public Methods:
        read : Read data from database file
        write: Write data to database file
    """

    _TABLE_NAME = "files"
    _CREATE_TABLE_CMD = f"""
    CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
        path TEXT PRIMARY KEY,
        size TEXT NOT NULL,
        last_modified TEXT NOT NULL,
        md5 TEXT NOT NULL,
        sha1 TEXT NOT NULL
    );
    """
    _TRUNCATE_TABLE_CMD = f"DELETE FROM {_TABLE_NAME};"
    _SELECT_TABLE_CMD = f"""
    SELECT path, size, last_modified, md5, sha1
    FROM {_TABLE_NAME};
    """
    _INSERT_TABLE_CMD = f"""
    INSERT INTO {_TABLE_NAME} (path, size, last_modified, md5, sha1)
    VALUES (?, ?, ?, ?, ?);
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> dict[str, FileStat]:
        """
        Read data from database file

        Returns:
            (dict[str, File_Props]): Existing path string-file property mapping
        """
        clear_print("Reading DB...")

        file_stats: dict[str, FileStat] = {}

        with self._open_db() as con:
            with con:
                con.execute(Db._CREATE_TABLE_CMD)

            cursor = con.execute(Db._SELECT_TABLE_CMD)
            data: list[DatabaseRow] = cursor.fetchall()

            for row in data:
                file_stats[row[0]] = FileStat.from_db_row(row)

        clear_print(f"Read {len(file_stats)} entries from DB")
        return file_stats

    def write(self, file_stats: list[FileStat]) -> None:
        """
        Write data to database file

        Args:
            file_stats (list[FileStat]): List of file stats to write to the db
        """
        clear_print(f"Writing all file data DB to {self.path}...")

        with self._open_db() as con:
            with con:
                con.execute(Db._TRUNCATE_TABLE_CMD)

            with con:
                con.executemany(
                    Db._INSERT_TABLE_CMD,
                    (file_stat.to_db_row() for file_stat in file_stats),
                )

    @contextmanager
    def _open_db(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager for opening the sqlite3 database

        Yields:
            (sqlite3.Connection): DB connection
        """
        con = sqlite3.connect(self.path)
        try:
            yield con
        finally:
            con.close()
