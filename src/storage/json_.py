"""
Module: Write to JSON

Public Functions:
    write_json
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List


def write_json(
    json_path: Path,
    duplication_list: List[Dict[str, Dict[str, int | Dict[str, str]] | List[str]]],
) -> None:
    """
    Write duplication stuff to JSON

    Args:
        json_path        {Path}: Path of JSON file
        duplication_list {List[Dict[str, Dict[str, int | Dict[str, str]] | List[str]]]}:
            List of duplication data
    """
    with json_path.open("w") as json_fp:
        json.dump(duplication_list, json_fp, indent=2)