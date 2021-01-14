"""
Module: Text output

Public Classes:
    Txt: Text output
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from progbar import clear_print


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

    def write(self, data: Iterable[str], indicator: str) -> None:
        """
        Write data to text file

        Args:
            data (Iterator[str]): Collection of file paths
        """
        clear_print(f"Writing {indicator} to {self.path}")

        with self.path.open("w") as fp:
            for new in data:
                print(new, file=fp)
