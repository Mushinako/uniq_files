"""
Module: Walk through the directory tree

Public Functions:
    make_tree: Make directory tree
    walk_tree: Get duplication data
"""

from collections import defaultdict
from pathlib import Path

from .data.duplication import Duplication
from .data.file_stat import FileStat, IdStat
from .dir_types.dir_ import DirPath
from .utils.byte import byte_shorten
from .utils.print_ import clear_print
from .utils.progress import ETA, Progress


def make_tree(base_path: Path) -> DirPath:
    """
    Make directory tree

    Args:
        base_path (pathlib.Path): Base directory path

    Returns:
        (DirPath): The tree!
    """
    clear_print("Calculating total size...")
    root_dir = DirPath(base_path)
    clear_print(f"Total file size: {root_dir.size:,} ({byte_shorten(root_dir.size)})")
    return root_dir


def walk_tree(
    root_dir: DirPath, existing_file_stats: dict[str, FileStat]
) -> tuple[list[Duplication], list[FileStat], list[str]]:
    """
    Get duplication data

    Args:
        base_path (pathlib.Path):
            Base directory path
        existing_file_stats (dict[str, FileStat]):
            Existing path string-file property mapping

    Returns:
        (list[Duplication]): All duplications
        (list[FileStat])   : All file properties
        (list[str])        : All new files
    """
    clear_print("Getting all file data...")
    total_progress = Progress(root_dir.size)
    eta = ETA(root_dir.size)
    file_stats, new_path_strs = root_dir.process_dir(
        existing_file_stats, total_progress, eta
    )
    clear_print(f"Found {len(file_stats)} files, of which {len(new_path_strs)} are new")

    clear_print("Finding duplicates...")
    potential_duplications: defaultdict[IdStat, list[str]] = defaultdict(list)

    for file_stat in file_stats:
        potential_duplications[file_stat.to_id_stat()].append(file_stat.path)

    duplications: list[Duplication] = []

    for id_stat, file_path_strs in potential_duplications.items():
        if len(file_path_strs) > 1:
            duplications.append(Duplication(*id_stat, file_path_strs))

    duplications.sort()

    clear_print(f"Found {len(duplications)} groups of duplicates")
    return duplications, file_stats, new_path_strs
