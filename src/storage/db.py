"""
Module: Reading from and writing to sqlite3 database

Public Functions:
    read_db  {Path -> dict[Path, File_Props]}
    write_db {Path, list[File_Props] -> None}
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

from ..types_.file_prop import File_Props


_TABLE_NAME = "files"
_CREATE_TABLE_CMD = f"""
CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (
    path TEXT PRIMARY KEY,
    path_type INTEGER NOT NULL,
    size TEXT NOT NULL,
    last_modified TEXT NOT NULL,
    md5 TEXT NOT NULL,
    sha1 TEXT NOT NULL
);
"""
_TRUNCATE_TABLE_CMD = f"DELETE FROM {_TABLE_NAME};"
_SELECT_TABLE_CMD = f"""
SELECT path, path_type, size, last_modified, md5, sha1
FROM {_TABLE_NAME};
"""
_INSERT_TABLE_CMD = f"""
INSERT INTO {_TABLE_NAME} (path, path_type, size, last_modified, md5, sha1)
VALUES (?, ?, ?, ?, ?, ?);
"""


def read_db(db_path: Path) -> dict[str, File_Props]:
    """
    Read database at given path and returns data in a dictionary

    Args:
        db_path {Path}: DB file path

    Returns:
        {dict[str, File_Props]}: Path-file property mapping
    """
    files_props: dict[str, File_Props] = {}
    with _open_db(db_path) as con:
        with con:
            con.execute(_CREATE_TABLE_CMD)
        cursor = con.execute(_SELECT_TABLE_CMD)
        data: list[tuple[str, int, str, str, str, str]] = cursor.fetchall()
        for path, _, size_str, last_modified_str, md5, sha1 in data:
            files_props[path] = File_Props(
                path, int(size_str), float(last_modified_str), md5, sha1
            )
    return files_props


def write_db(files_props: list[File_Props], db_path: Path) -> None:
    """
    Write database at given path

    Args:
        files_props {list[File_Props]}: Stuff to be written to the database
        db_path     {Path}            : DB file path
    """
    with _open_db(db_path) as con:
        with con:
            con.execute(_TRUNCATE_TABLE_CMD)
        with con:
            con.executemany(
                _INSERT_TABLE_CMD,
                (
                    (
                        str(fp.path),
                        str(fp.size),
                        str(fp.last_modified),
                        fp.md5,
                        fp.sha1,
                    )
                    for fp in files_props
                ),
            )


@contextmanager
def _open_db(db_path: Path) -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for the sqlite3 database

    Args:
        db_path {Path}: DB file path

    Yields:
        {sqlite3.Connection}: DB connection
    """
    con = sqlite3.connect(db_path)
    try:
        yield con
    finally:
        con.close()
