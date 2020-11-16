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
from typing import Dict, Generator, List, Tuple

from ..types_.dir_types import Union_Path
from ..types_.file_prop import PATH_CLASS_MAP, File_Props, Path_Type


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


def read_db(db_path: Path) -> Dict[Union_Path, File_Props]:
    """
    Read database at given path and returns data in a dictionary

    Args:
        db_path {Path}: DB file path

    Returns:
        {dict[Union_Path, File_Props]}: Path-file property mapping
    """
    files_props: Dict[Union_Path, File_Props] = {}
    with _open_db(db_path) as con:
        with con:
            con.execute(_CREATE_TABLE_CMD)
        cursor = con.execute(_SELECT_TABLE_CMD)
        data: List[Tuple[str, int, str, str, str, str]] = cursor.fetchall()
        for path_str, path_type_int, size_str, last_modified_str, md5, sha1 in data:
            path_type = Path_Type(path_type_int)
            Path_Class = PATH_CLASS_MAP[path_type]
            path: Union_Path = Path_Class(path_str)
            files_props[path] = File_Props(
                path, path_type, int(size_str), int(last_modified_str), md5, sha1
            )
    return files_props


def write_db(db_path: Path, files_props: List[File_Props]) -> None:
    """
    Write database at given path

    Args:
        db_path     {Path}            : DB file path
        files_props {list[File_Props]}: Stuff to be written to the database
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
                        fp.path_type.value,
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
