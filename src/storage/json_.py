"""
Module: Writing to JSON file

Public Classes:
    Json: JSON output

Public Functions:
    write_jsons: Write JSON data into corresponding files
"""

from json import dump as json_dump
from pathlib import Path
from typing import Optional

from progbar import clear_print

from ..config import SMALL_SIZE, LARGE_SIZE
from ..data.duplication import Duplication


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

    def write(self, data: list[Duplication], indicator: str) -> None:
        """
        Write duplication data to JSON file

        Args:
            data      (list[Duplication]): Duplication data to be written
            indicator (str)              : Duplication name. For printing only
        """
        clear_print(f"Writing {indicator} JSON to {self.path}...")

        with self.path.open("w") as fp:
            json_dump(
                [duplication.to_json_dict() for duplication in data],
                fp,
                indent=2,
            )


def write_json(
    duplications: list[Duplication],
    dup_json: Json,
    *,
    small_json: Optional[Json] = None,
    large_json: Optional[Json] = None,
    small_size: int = SMALL_SIZE,
    large_size: int = LARGE_SIZE,
) -> None:
    """
    Write JSON data into corresponding files

    Args:
        duplicatins (list[Duplication]):
            All duplications
        dup_json (Json):
            Base JSON writer
        *
        small_json (Json):
            Small JSON writer
        large_json (Json):
            Large JSON writer
        small_size (int):
            Maximum file size to qualify as a small file
        large_size (int):
            Minimum file size to qualify as a large file
    """
    duplications.sort()

    if small_json is None and large_json is None:
        dup_json.write(duplications, "duplications")
        return

    duplication_iter = iter(duplications)

    if small_json is not None:
        small_duplications: list[Duplication] = []
        not_small_duplications: list[Duplication] = []

        for duplication in duplication_iter:
            if duplication.size > small_size:
                not_small_duplications.append(duplication)
                break
            else:
                small_duplications.append(duplication)

        small_json.write(small_duplications, "small duplications")

        duplication_iter = iter(not_small_duplications + list(duplication_iter))

    if large_json is not None:
        large_duplications: list[Duplication] = []
        not_large_duplications: list[Duplication] = []

        for duplication in duplication_iter:
            if duplication.size > large_size:
                large_duplications.append(duplication)
                break
            else:
                not_large_duplications.append(duplication)

        large_json.write(
            large_duplications + list(duplication_iter), "large duplications"
        )

        duplication_iter = iter(not_large_duplications)

    dup_json.write(list(duplication_iter), "duplications left")
