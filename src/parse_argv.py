"""
Module: Parsing command-line arguments

Public Functions:
    parse_argv: Parse command-line arguments
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

from .config import SMALL_SIZE, LARGE_SIZE
from .dir_types.utils.error import NotAFileError
from .storage.db import Db
from .storage.json_ import Json
from .storage.txt import Txt


def parse_argv() -> _Args:
    """
    Parse command-line arguments

    Returns:
        (_Args): Namespace object for all arguments
    """
    parser = ArgumentParser(description="Check file duplicates under some base path")

    input_group = parser.add_argument_group("inputs")
    input_group.add_argument(
        "-f",
        "--dir-path",
        type=_full_path,
        required=True,
        help="base directory path",
        dest="dir_path",
    )

    output_group = parser.add_argument_group("outputs")
    output_group.add_argument(
        "-d",
        "--db-path",
        type=_db,
        required=True,
        help="file database path",
        dest="db",
    )
    output_group.add_argument(
        "-t",
        "--new-txt-path",
        type=_txt,
        help="new files list text path (Optional)",
        dest="new_txt",
    )
    output_group.add_argument(
        "-e",
        "--empty-txt-path",
        type=_txt,
        help="empty directories list text path (Optional)",
        dest="empty_txt",
    )

    json_output_group = output_group.add_argument_group("JSON outputs")
    json_output_group.add_argument(
        "-j",
        "--dup-json-path",
        type=_json,
        required=True,
        help="duplication JSON path",
        dest="dup_json",
    )
    json_output_group.add_argument(
        "-js",
        "--small-json-path",
        type=_json,
        help="small file duplication JSON path (Optional)",
        dest="small_json",
    )
    json_output_group.add_argument(
        "-jl",
        "--large-json-path",
        type=_json,
        help="large file duplication JSON path (Optional)",
        dest="large_json",
    )

    config_group = parser.add_argument_group("configs")
    config_group.add_argument(
        "-s",
        "--small-size",
        default=SMALL_SIZE,
        type=int,
        help=f"maximum file size to qualify as a small file (Default: {SMALL_SIZE:,} bytes)",
        dest="small_size",
    )
    config_group.add_argument(
        "-l",
        "--large-size",
        default=LARGE_SIZE,
        type=int,
        help=f"minimum file size to qualify as a large file (Default: {LARGE_SIZE:,} bytes)",
        dest="large_size",
    )

    args = parser.parse_args(namespace=_Args())
    args.prepare_argv()

    return args


class _Args(Namespace):
    """
    Command-line arguments object, for type annotations only
    """

    dir_path: Path
    db: Db
    new_txt: Optional[Txt]
    empty_txt: Optional[Txt]
    dup_json: Json
    small_json: Optional[Json]
    large_json: Optional[Json]
    small_size: int
    large_size: int

    def prepare_argv(self) -> None:
        """
        Check arguments validity and make preparations
        """
        self._check_input_dir(self.dir_path)

        self._prepare_output_file(self.db.path)

        if self.new_txt is not None:
            self._prepare_output_file(self.new_txt.path)
        if self.empty_txt is not None:
            self._prepare_output_file(self.empty_txt.path)

        self._prepare_output_file(self.dup_json.path)
        if self.small_json is not None:
            self._prepare_output_file(self.small_json.path)
        if self.large_json is not None:
            self._prepare_output_file(self.large_json.path)

    @staticmethod
    def _check_input_dir(dir_path: Path) -> None:
        """
        Check if an input directory exists

        Args:
            dir_path (pathlib.Path): The directory path to be checked
        """
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{dir_path} is not a directory")

    @staticmethod
    def _prepare_output_file(file_path: Path) -> None:
        """
        Prepare output file

        Args:
            file_path (pathlib.Path): The file path to be prepared
        """
        if file_path.exists() and not file_path.is_file():
            raise NotAFileError(f"{file_path} exists but is not a file")

        file_path.parent.mkdir(parents=True, exist_ok=True)


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
