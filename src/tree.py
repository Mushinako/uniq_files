"""
Module: Walk through the directory tree

Public Functions:
    make_tree: Make directory tree
    walk_tree: Get duplication data
"""

from collections import defaultdict
from pathlib import Path
from traceback import print_exc

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
        (list[str])        : Records to be removed from the database
    """
    clear_print("Getting all file data...")
    total_progress = Progress(root_dir.size)
    eta = ETA(root_dir.size)
    leftover_file_stats = existing_file_stats.copy()
    new_file_stats: list[FileStat] = []

    try:
        root_dir.process_dir(leftover_file_stats, total_progress, eta, new_file_stats)
    except KeyboardInterrupt:
        clear_print("KeyboardInterrupt detected; stopping...")
        # Don't remove anything from the database if the procedure is interrupted
        leftover_file_stats = {}
    except Exception:
        clear_print("\nException occurred!")
        print_exc()
        print()
        leftover_file_stats = {}

    new_file_stats.sort()
    clear_print(
        f"Found {root_dir.length} files, of which {len(new_file_stats)} are new"
    )

    clear_print("Finding duplicates...")
    potential_duplications: defaultdict[IdStat, list[str]] = defaultdict(list)

    for path_str, file_stat in existing_file_stats.items():
        if path_str in leftover_file_stats:
            continue
        potential_duplications[file_stat.to_id_stat()].append(path_str)

    for file_stat in new_file_stats:
        potential_duplications[file_stat.to_id_stat()].append(file_stat.path)

    duplications: list[Duplication] = []

    for id_stat, file_path_strs in potential_duplications.items():
        if len(file_path_strs) > 1:
            duplications.append(Duplication(*id_stat, file_path_strs))

    duplications.sort()

    clear_print(f"Found {len(duplications)} groups of duplicates")
    return duplications, new_file_stats, sorted(leftover_file_stats)
