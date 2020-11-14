"""
"""
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator, List, Tuple

from .inspect_file import File_Data

TABLE_NAME = "files"
CREATE_TABLE_CMD = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    path TEXT PRIMARY KEY,
    size TEXT NOT NULL,
    last_modified TEXT NOT NULL,
    md5 TEXT NOT NULL,
    sha1 TEXT NOT NULL,
);
"""
TRUNCATE_TABLE_CMD = f"DELETE FROM {TABLE_NAME};"
SELECT_TABLE_CMD = f"""
SELECT path, size, last_modified, md5, sha1
FROM {TABLE_NAME};
"""
INSERT_TABLE_CMD = f"""
INSERT INTO {TABLE_NAME} (path, size, last_modified, md5, sha1)
VALUES (?, ?, ?, ?, ?);
"""


@contextmanager
def open_database(path: Path) -> Generator[sqlite3.Connection, None, None]:
    """"""
    con = sqlite3.connect(path)
    try:
        yield con
    finally:
        con.close()


def read_database(path: Path) -> List[Tuple[str, str, str, str, str]]:
    """"""
    with open_database(path) as con:
        with con:
            con.execute(CREATE_TABLE_CMD)
        cursor = con.execute(SELECT_TABLE_CMD)
        return cursor.fetchall()


def write_database(path: Path, data: List[File_Data]) -> None:
    with open_database(path) as con:
        with con:
            con.execute(TRUNCATE_TABLE_CMD)
            con.executemany(
                INSERT_TABLE_CMD,
                [
                    (str(d.path), str(d.size), str(d.last_modified), d.md5, d.sha1)
                    for d in data
                ],
            )
