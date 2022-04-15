"""
Module: Writing to JSON file

Public Classes:
    Json: JSON output

Public Functions:
    write_jsons: Write JSON data into corresponding files
"""

from pathlib import Path

from progbar import clear_print
from yaml import safe_dump

from src.config import SMALL_SIZE, LARGE_SIZE
from src.data.duplication import Duplication


class Yaml:
    """
    YAML output

    Args:
        path (pathlib.Path): YAML file path

    Public Attributes:
        path (pathlib.Path): YAML file path

    Public Methods:
        write: Write duplication data to YAML file
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, data: list[Duplication], indicator: str) -> None:
        """
        Write duplication data to YAML file

        Args:
            data      (list[Duplication]): Duplication data to be written
            indicator (str)              : Duplication name. For printing only
        """
        clear_print(f"Writing {indicator} YAML to {self.path}...")

        with self.path.open("w") as fp:
            safe_dump([duplication.to_json_dict() for duplication in data], fp)


def write_dup(
    duplications: list[Duplication],
    dup_yaml: Yaml,
    *,
    small_yaml: None | Yaml = None,
    large_yaml: None | Yaml = None,
    small_size: int = SMALL_SIZE,
    large_size: int = LARGE_SIZE,
) -> None:
    """
    Write YAML data into corresponding files

    Args:
        duplicatins (list[Duplication]):
            All duplications
        dup_yaml (Yaml):
            Base YAML writer
        *
        small_yaml (Yaml):
            Small YAML writer
        large_yaml (Yaml):
            Large YAML writer
        small_size (int):
            Maximum file size to qualify as a small file
        large_size (int):
            Minimum file size to qualify as a large file
    """
    duplications.sort()

    if small_yaml is None and large_yaml is None:
        dup_yaml.write(duplications, "duplications")
        return

    duplication_iter = iter(duplications)

    if small_yaml is not None:
        small_duplications: list[Duplication] = []
        not_small_duplications: list[Duplication] = []

        for duplication in duplication_iter:
            if duplication.size > small_size:
                not_small_duplications.append(duplication)
                break
            else:
                small_duplications.append(duplication)

        small_yaml.write(small_duplications, "small duplications")

        duplication_iter = iter(not_small_duplications + list(duplication_iter))

    if large_yaml is not None:
        large_duplications: list[Duplication] = []
        not_large_duplications: list[Duplication] = []

        for duplication in duplication_iter:
            if duplication.size > large_size:
                large_duplications.append(duplication)
                break
            else:
                not_large_duplications.append(duplication)

        large_yaml.write(
            large_duplications + list(duplication_iter), "large duplications"
        )

        duplication_iter = iter(not_large_duplications)

    dup_yaml.write(list(duplication_iter), "duplications left")
