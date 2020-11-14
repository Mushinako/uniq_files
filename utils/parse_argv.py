"""
"""
from pathlib import Path
from argparse import ArgumentParser, Namespace


class _Args(Namespace):
    """"""

    base_path: Path
    dup_json_path: Path
    file_database_path: Path


def full_path(arg: str) -> Path:
    return Path(arg).resolve()


def parse_argv() -> _Args:
    """"""
    parser = ArgumentParser(description="Check file duplicates under some base path")
    parser.add_argument("base_path", type=full_path, help="Base path")
    parser.add_argument("dup_json_path", type=full_path, help="Duplication JSON path")
    parser.add_argument("file_database_path", type=full_path, help="File database path")
    args: _Args = parser.parse_args()

    _prepare_argv(args)

    return args


def _prepare_argv(args: _Args) -> None:
    """"""
    if not args.base_path.is_dir():
        raise FileNotFoundError(f"`base_path` not a directory: {args.base_path}")
    if args.dup_json_path.exists() and not args.dup_json_path.is_file():
        raise FileNotFoundError(f"`dup_json_path` not a file: {args.dup_json_path}")
    if args.file_database_path.exists() and not args.file_database_path.is_file():
        raise FileNotFoundError(
            f"`file_database_path` not a file: {args.file_database_path}"
        )

    args.dup_json_path.parent.mkdir(parents=True, exist_ok=True)
    args.file_database_path.parent.mkdir(parents=True, exist_ok=True)
