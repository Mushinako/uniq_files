#!/usr/bin/env python3
from utils.parse_argv import parse_argv
from utils.get_duplicates import get_duplicates, write_duplicates


def main() -> None:
    """"""
    base_path, json_path = parse_argv()
    duplication_data = get_duplicates(base_path)
    write_duplicates(json_path, duplication_data)


if __name__ == "__main__":
    main()