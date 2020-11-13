from json import dump as json_dump
from collections import defaultdict
from typing import Dict, List, Tuple

from utils.get_file import File_Property, iter_walk, get_file_properties


def get_info(base_path) -> Tuple[List[Dict], List[Tuple[str, int, int, str, str, str]]]:
    """
    Get duplication info under a base path
    """

    all_files_dict: defaultdict[File_Property, List[str]] = defaultdict(list)
    all_files_list: List[Tuple[str, int, int, str, str, str]] = []
    print()
    try:
        for id_, count, path in iter_walk(base_path):
            properties = get_file_properties(path, id_, count)
            all_files_dict[properties].append(str(path))
            all_files_list.append(
                (
                    str(path),
                    path.stat().st_ctime,
                    properties.size,
                    properties.md5_,
                    properties.sha1_,
                    properties.sha512_,
                )
            )
    except KeyboardInterrupt:
        print("\r\x1b[KStopping...")
    print("\r\x1b[K")
    print()

    duplicates_list: List[Dict] = []
    for properties, paths in all_files_dict.items():
        if len(paths) == 1:
            continue
        paths.sort()
        properties_dict = {
            "size": properties.size,
            "hashes": {
                "md5": properties.md5_,
                "sha1": properties.sha1_,
                "sha512": properties.sha512_,
            },
        }
        duplication_entry = {
            "properties": properties_dict,
            "paths": paths,
        }
        duplicates_list.append(duplication_entry)

    duplicates_list.sort(key=lambda d: d["properties"]["size"])
    return duplicates_list, all_files_list


def write_duplicates(json_path: str, duplication_data: List[Dict]) -> None:
    """"""
    with open(json_path, "w") as json_fp:
        json_dump(duplication_data, json_fp, indent=4)
