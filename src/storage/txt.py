"""
Module: Write to text

Public Functions:
    write_txt
"""
from __future__ import annotations
from pathlib import Path


def write_txt(new_list: list[str], new_txt_path: Path) -> None:
    """
    Write new stuff to file

    Args:
        new_list     (list[str])   : List of new file paths
        new_txt_path (pathlib.Path): Path of text file for new files
    """
    with new_txt_path.open("w") as new_txt_fp:
        for new in new_list:
            print(new, file=new_txt_fp)
