"""
Module: Text output

Public Classes:
    Txt: Text output
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

from ..utils.print_ import clear_print


class Txt:
    """
    Text output

    Args:
        path (pathlib.Path): Text file path

    Public Attributes:
        path (pathlib.Path): Text file path

    Public Methods:
        write: Write new file data to text file
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, data: Iterator[str]) -> None:
        """
        Write new file data to text file

        Args:
            data (Iterator[str]): List of new file pathss
        """
        clear_print(f"Writing new file paths to {self.path}")

        with self.path.open("w") as fp:
            for new in data:
                print(new, file=fp)
