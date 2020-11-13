from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Tuple


class Args(Namespace):
    """
    Command-line arguments namespace

    Properties:
        base_path        {Path} - The path of the base directory whose descendants are checked
        output_base_path {str}  - The output base path
    """

    def __init__(self) -> None:
        self.base_path: Path
        self.output_base_path: str


def parse_argv() -> Tuple[Path, Path, Path]:
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
        "output_base_path",
        help="The path of json to/from which duplication data is stored/read",
    )

    args = parser.parse_args(namespace=Args())

    base_path = args.base_path.resolve()
    json_path = Path(args.output_base_path + ".json").resolve()
    db_path = Path(args.output_base_path + ".sqlite3").resolve()
    base_path.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if not base_path.is_dir():
        raise ValueError(f"{base_path} should be a directory.")
    if json_path.exists() and not json_path.is_file():
        raise ValueError(f"{json_path} should be a file.")
    if db_path.exists() and not db_path.is_file():
        raise ValueError(f"{db_path} should be a file.")

    return base_path, json_path, db_path
