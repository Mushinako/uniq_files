"""
Module: Write to JSON

Public Functions:
    write_json
    write_json_w_small
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Union

from ..parse_argv import SMALL_SIZE


def write_json(
    dup_list: list[tuple[tuple[int, str, str], list[str]]],
    dup_json_path: Path,
) -> None:
    """
    Write duplication stuff to JSON

    Args:
        dup_list      {list[tuple[tuple[int, str, str], list[str]]]}:
            List of duplication data
        dup_json_path {pathlib.Path}: Path of JSON file for large files
    """
    # Get duplications
    formatted_data = [
        {
            "properties": {
                "size": size,
                "hashes": {
                    "md5": md5,
                    "sha1": sha1,
                },
            },
            "paths": file_paths,
        }
        for (size, md5, sha1), file_paths in dup_list
    ]

    with dup_json_path.open("w") as dup_json_fp:
        json.dump(formatted_data, dup_json_fp, indent=2)


def write_json_w_small(
    dup_list: list[tuple[tuple[int, str, str], list[str]]],
    dup_json_path: Path,
    small_json_path: Path,
    small_size: int = SMALL_SIZE,
) -> None:
    """
    Write duplication stuff to JSON, separating large and small files

    Args:
        dup_list        {list[tuple[tuple[int, str, str], list[str]]]}:
            List of duplication data
        dup_json_path   {pathlib.Path}: Path of JSON file for large files
        small_json_path {pathlib.Path}: Path of JSON file for small files
        small_size      {int}         : Threshold above which file is considered "large"
    """
    small_list: list[
        dict[str, Union[dict[str, Union[int, dict[str, str]]], list[str]]]
    ] = []
    large_list: list[
        dict[str, Union[dict[str, Union[int, dict[str, str]]], list[str]]]
    ] = []

    dup_iter = iter(dup_list)

    for (size, md5, sha1), file_paths in dup_iter:
        formatted_datum = {
            "properties": {
                "size": size,
                "hashes": {
                    "md5": md5,
                    "sha1": sha1,
                },
            },
            "paths": file_paths,
        }
        if size > small_size:
            large_list.append(formatted_datum)
            break
        else:
            small_list.append(formatted_datum)

    large_list += [
        {
            "properties": {
                "size": size,
                "hashes": {
                    "md5": md5,
                    "sha1": sha1,
                },
            },
            "paths": file_paths,
        }
        for (size, md5, sha1), file_paths in dup_iter
    ]

    with dup_json_path.open("w") as dup_json_fp:
        json.dump(large_list, dup_json_fp, indent=2)
    with small_json_path.open("w") as small_json_fp:
        json.dump(small_list, small_json_fp, indent=2)
