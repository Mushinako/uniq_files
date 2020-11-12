#!/usr/bin/env python3
from json import dump as json_dump, load as json_load

from utils.parse_argv import parse_argv
from utils.get_duplicates import get_duplicates, write_duplicates


def main() -> None:
    """"""
    base_path, json_path = parse_argv()
    duplication_data = get_duplicates(base_path)
    with open(json_path, "w") as json_fp:
        json_dump(duplication_data, json_fp, indent=4)


if __name__ == "__main__":
    main()