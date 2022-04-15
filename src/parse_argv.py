"""
Module: Parsing command-line arguments

Public Functions:
    parse_argv: Parse command-line arguments
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from .config import SMALL_SIZE, LARGE_SIZE
from .dir_types.utils.error import NotAFileError
from .storage.db import Db
from .storage.yaml_ import Yaml
from .storage.txt import Txt


def parse_argv() -> _Args:
    """
    Parse command-line arguments

    Returns:
        (_Args): Namespace object for all arguments
    """
    parser = ArgumentParser(description="check file duplicates under some base path")

    input_group = parser.add_argument_group("inputs")
    input_group.add_argument(
        "dir_path",
        type=_full_path,
        help="base directory path",
        metavar="dir-path",
    )

    data_output_group = parser.add_argument_group("outputs")
    data_output_group.add_argument(
        "-d",
        "--db-path",
        type=_db,
        help="file database path",
        dest="db",
    )
    data_output_group.add_argument(
        "-tn",
        "--new-txt-path",
        type=_txt,
        help="new files list text path (optional)",
        dest="new_txt",
    )
    data_output_group.add_argument(
        "-te",
        "--empty-txt-path",
        type=_txt,
        help="empty directories list text path (optional)",
        dest="empty_txt",
    )

    dup_output_group = parser.add_argument_group("duplication outputs")
    dup_output_group.add_argument(
        "-o",
        "--dup-yaml",
        type=_yml,
        required=True,
        help="duplication YAML path",
        dest="dup_yaml",
    )
    dup_output_group.add_argument(
        "-os",
        "--small-yaml",
        type=_yml,
        help="small file duplication YAML path (optional)",
        dest="small_yaml",
    )
    dup_output_group.add_argument(
        "-ol",
        "--large-yaml",
        type=_yml,
        help="large file duplication YAML path (optional)",
        dest="large_yaml",
    )

    config_group = parser.add_argument_group("configs")
    config_group.add_argument(
        "-ss",
        "--small-size",
        default=SMALL_SIZE,
        type=int,
        help=f"maximum file size for small files (Default: {SMALL_SIZE:,} bytes)",
        dest="small_size",
    )
    config_group.add_argument(
        "-sl",
        "--large-size",
        default=LARGE_SIZE,
        type=int,
        help=f"minimum file size for large files (Default: {LARGE_SIZE:,} bytes)",
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
    db: None | Db
    new_txt: None | Txt
    empty_txt: None | Txt
    dup_yaml: Yaml
    small_yaml: None | Yaml
    large_yaml: None | Yaml
    small_size: int
    large_size: int

    def prepare_argv(self) -> None:
        """
        Check arguments validity and make preparations
        """
        self._check_input_dir(self.dir_path)

        if self.db is not None:
            self._prepare_output_file(self.db.path)

        if self.new_txt is not None:
            self._prepare_output_file(self.new_txt.path)
        if self.empty_txt is not None:
            self._prepare_output_file(self.empty_txt.path)

        self._prepare_output_file(self.dup_yaml.path)
        if self.small_yaml is not None:
            self._prepare_output_file(self.small_yaml.path)
        if self.large_yaml is not None:
            self._prepare_output_file(self.large_yaml.path)

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


def _yml(arg: str) -> Yaml:
    """
    Helper function for resolving a database path to YAML output object

    Args:
        arg (str): Command-line argument

    Returns:
        (Yaml): YAML output object
    """
    return Yaml(Path(arg).resolve())


def _txt(arg: str) -> Txt:
    """
    Helper function for resolving a database path to text output object

    Args:
        arg (str): Command-line argument

    Returns:
        (Txt): Text output object
    """
    return Txt(Path(arg).resolve())
