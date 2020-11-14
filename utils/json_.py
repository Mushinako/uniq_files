"""
"""
import json
from pathlib import Path
from typing import List


def write_json(path: Path, data: List) -> None:
    """"""
    with path.open("w") as json_fp:
        json.dump(data, json_fp, indent=4)