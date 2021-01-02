"""
Module: Writing to JSON file

Public Classes:
    Json: JSON output

Public Functions:
    split_duplication_data: Split duplications into large- and small-file lists
"""

from json import dump as json_dump
from pathlib import Path

from ..data.duplication import Duplication
from ..utils.print_ import clear_print


class Json:
    """
    JSON output

    Args:
        path (pathlib.Path): JSON file path

    Public Attributes:
        path (pathlib.Path): JSON file path

    Public Methods:
        write: Write duplication data to JSON file
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, duplications: list[Duplication], duplication_name: str) -> None:
        """
        Write duplication data to JSON file

        Args:
            duplications     (list[Duplication]): Duplication data to be written
            duplication_name (str)              : Duplication name. For printing only
        """
        clear_print(f"Writing {duplication_name} JSON to {self.path}...")

        with self.path.open("w") as fp:
            json_dump(
                [duplication.to_json_dict() for duplication in duplications],
                fp,
                indent=2,
            )


def split_duplication_data(
    duplications: list[Duplication], small_size: int
) -> tuple[list[Duplication], list[Duplication]]:
    """
    Split duplications into large- and small-file lists, where large-file list
        contains all the duplications with file sizes strictly larger than
        `small_size`, and small-file list containing the rest

    Args:
        duplicatins (list[Duplication]):
            All duplications
        small_size (int):
            Threshold beyond which a file is considered large

    Returns:
        (list[Duplication]): Large duplication lists
        (list[Duplication]): Small duplication lists
    """
    duplication_iter = iter(sorted(duplications))

    large_duplications: list[Duplication] = []
    small_duplications: list[Duplication] = []

    for duplication in duplication_iter:
        if duplication.size > small_size:
            large_duplications.append(duplication)
            break
        else:
            small_duplications.append(duplication)

    large_duplications += list(duplication_iter)

    return large_duplications, small_duplications
