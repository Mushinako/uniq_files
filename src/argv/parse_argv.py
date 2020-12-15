"""
Module: Parsing command-line arguments

Public Functions:
    parse_argv {None -> _Args}

Public Constants:
    SMALL_SIZE
"""
from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser, Namespace
from typing import Optional

SMALL_SIZE = 4


def parse_argv() -> _Args:
    """
    Parse command-line arguments

    Returns:
        {_Args}: Namespace object for all arguments
    """
    parser = ArgumentParser(description="Check file duplicates under some base path")
    parser.add_argument(
        "-f",
        "--dir-path",
        type=_full_path,
        required=True,
        help="Base directory path",
        dest="dir_path",
    )
    parser.add_argument(
        "-j",
        "--dup-json-path",
        type=_full_path,
        required=True,
        help="Duplication JSON path",
        dest="dup_json_path",
    )
    parser.add_argument(
        "-b",
        "--small-json-path",
        type=_full_path,
        help="Small file duplication JSON path (Optional)",
        dest="small_json_path",
    )
    parser.add_argument(
        "-d",
        "--db-path",
        type=_full_path,
        required=True,
        help="File database path",
        dest="db_path",
    )
    parser.add_argument(
        "-s",
        "--small-size",
        default=SMALL_SIZE,
        type=int,
        help="Maximum file size to qualify as a small file (Default: 4 bytes)",
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
    dup_json_path: Path
    small_json_path: Optional[Path]
    db_path: Path
    small_size: int


def _full_path(arg: str) -> Path:
    """
    Helper function for resolving all the paths to absolute Path objects

    Args:
        arg {str}: Command-line argument

    Returns:
        {Path}: Absolute Path object
    """
    return Path(arg).resolve()


def _prepare_argv(args: _Args) -> None:
    """
    Check arguments validity and make preparations

    args {_Args}: Parsed command-line args
    """
    if not args.dir_path.is_dir():
        raise FileExistsError(
            f"`dir_path` exists but is not a directory: {args.dir_path}"
        )

    if args.dup_json_path.exists() and not args.dup_json_path.is_file():
        raise FileExistsError(
            f"`dup_json_path` exists but is not a file: {args.dup_json_path}"
        )
    args.dup_json_path.parent.mkdir(parents=True, exist_ok=True)

    if args.small_json_path is not None:
        if args.small_json_path.exists() and not args.small_json_path.is_file():
            raise FileExistsError(
                f"`small_json_path` exists but is not a file: {args.small_json_path}"
            )
        args.small_json_path.parent.mkdir(parents=True, exist_ok=True)

    if args.db_path.exists() and not args.db_path.is_file():
        raise FileExistsError(f"`db_path` exists but is not a file: {args.db_path}")
    args.db_path.parent.mkdir(parents=True, exist_ok=True)
