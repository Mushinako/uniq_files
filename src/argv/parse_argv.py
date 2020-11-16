"""
Module: Parsing command-line arguments

Public Functions:
    parse_argv {None -> _Args}
"""
from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser, Namespace


def parse_argv() -> _Args:
    """
    Parse command-line arguments

    Returns:
        {_Args}: Namespace object for all arguments
    """
    parser = ArgumentParser(description="Check file duplicates under some base path")
    parser.add_argument("base_path", type=_full_path, help="Base path")
    parser.add_argument("json_path", type=_full_path, help="Duplication JSON path")
    parser.add_argument("db_path", type=_full_path, help="File database path")
    args = parser.parse_args(namespace=_Args())

    _prepare_argv(args)

    return args


class _Args(Namespace):
    """
    Command-line arguments object, for type annotations only
    """

    base_path: Path
    json_path: Path
    db_path: Path


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
    if not args.base_path.is_dir():
        raise FileNotFoundError(f"`base_path` not a directory: {args.base_path}")
    if args.json_path.exists() and not args.json_path.is_file():
        raise FileNotFoundError(f"`dup_json_path` not a file: {args.json_path}")
    if args.db_path.exists() and not args.db_path.is_file():
        raise FileNotFoundError(f"`file_database_path` not a file: {args.db_path}")

    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.db_path.parent.mkdir(parents=True, exist_ok=True)
