from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Tuple


class Args(Namespace):
    """
    Command-line arguments namespace

    Properties:
        base_path {Path} - The path of the base directory whose descendants are checked
        json_path {Path} - The path of json to/from which duplication data is stored/read
    """

    def __init__(self) -> None:
        self.base_path: Path
        self.json_path: Path


def parse_argv() -> Tuple[Path, Path]:
    """
    Parse command-line arguments
    """
    parser = ArgumentParser(description="Specify base path to check")
    parser.add_argument(
        "base_path",
        type=Path,
        help="The base path whose descendants are checked",
    )
    parser.add_argument(
        "json_path",
        type=Path,
        help="The path of json to/from which duplication data is stored/read",
    )

    args = parser.parse_args(namespace=Args())

    base_path = args.base_path.resolve()
    json_path = args.json_path.resolve()
    base_path.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    if not base_path.is_dir():
        raise ValueError(f"{base_path} should be a directory.")
    if json_path.exists() and not json_path.is_file():
        raise ValueError(f"{json_path} should be a file.")

    return base_path, json_path
