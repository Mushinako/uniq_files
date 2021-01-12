"""
Module: Parsing command-line arguments

Public Functions:
    parse_argv: Parse command-line arguments

Public Constants:
    SMALL_SIZE (int): Number of bytes beyond which a file is not considered "small"
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

from .storage.db import Db
from .storage.json_ import Json
from .storage.txt import Txt

SMALL_SIZE = 4


def parse_argv() -> _Args:
    """
    Parse command-line arguments

    Returns:
        (_Args): Namespace object for all arguments
    """
    parser = ArgumentParser(description="Check file duplicates under some base path")
    parser.add_argument(
        "-f",
        "--dir-path",
        type=_full_path,
        required=True,
        help="base directory path",
        dest="dir_path",
    )
    parser.add_argument(
        "-d",
        "--db-path",
        type=_db,
        required=True,
        help="file database path",
        dest="db",
    )
    parser.add_argument(
        "-j",
        "--dup-json-path",
        type=_json,
        required=True,
        help="duplication JSON path",
        dest="dup_json",
    )
    parser.add_argument(
        "-b",
        "--small-json-path",
        type=_json,
        help="small file duplication JSON path (Optional)",
        dest="small_json",
    )
    parser.add_argument(
        "-n",
        "--new-txt-path",
        type=_txt,
        help="new file text list",
        dest="new_txt",
    )
    parser.add_argument(
        "-s",
        "--small-size",
        default=SMALL_SIZE,
        type=int,
        help="maximum file size to qualify as a small file (Default: 4 bytes)",
        dest="small_size",
    )
    args = parser.parse_args(namespace=_Args())

    _prepare_argv(args)

    return args


class _Args(Namespace):
    """
    Command-line arguments object, for type annotations only
    """

    dir_path: Path
    db: Db
    dup_json: Json
    small_json: Optional[Json]
    new_txt: Optional[Txt]
    small_size: int


def _full_path(arg: str) -> Path:
    """
    Helper function for resolving all the paths to absolute Path objects

    Args:
        arg (str): Command-line argument

    Returns:
        (pathlib.Path): Absolute Path object
    """
    return Path(arg).resolve()


def _db(arg: str) -> Db:
    """
    Helper function for resolving a database path to database I/O object

    Args:
        arg (str): Command-line argument

    Returns:
        (Db): Database I/O object
    """
    return Db(Path(arg).resolve())


def _json(arg: str) -> Json:
    """
    Helper function for resolving a database path to JSON output object

    Args:
        arg (str): Command-line argument

    Returns:
        (Json): JSON output object
    """
    return Json(Path(arg).resolve())


def _txt(arg: str) -> Txt:
    """
    Helper function for resolving a database path to text output object

    Args:
        arg (str): Command-line argument

    Returns:
        (Txt): Text output object
    """
    return Txt(Path(arg).resolve())


def _prepare_argv(args: _Args) -> None:
    """
    Check arguments validity and make preparations

    Args:
        args (_Args): Parsed command-line args
    """
    if not args.dir_path.is_dir():
        raise NotADirectoryError(
            f"`dir_path` exists but is not a directory: {args.dir_path}"
        )

    if args.db.path.exists() and not args.db.path.is_file():
        raise FileExistsError(f"`db_path` exists but is not a file: {args.db.path}")
    args.db.path.parent.mkdir(parents=True, exist_ok=True)

    if args.dup_json.path.exists() and not args.dup_json.path.is_file():
        raise FileExistsError(
            f"`dup_json_path` exists but is not a file: {args.dup_json.path}"
        )
    args.dup_json.path.parent.mkdir(parents=True, exist_ok=True)

    if args.small_json is not None:
        if args.small_json.path.exists() and not args.small_json.path.is_file():
            raise FileExistsError(
                f"`small_json_path` exists but is not a file: {args.small_json.path}"
            )
        args.small_json.path.parent.mkdir(parents=True, exist_ok=True)

    if args.new_txt is not None:
        if args.new_txt.path.exists() and not args.new_txt.path.is_file():
            raise FileExistsError(
                f"`new_txt_path` exists but is not a file: {args.new_txt.path}"
            )
        args.new_txt.path.parent.mkdir(parents=True, exist_ok=True)
