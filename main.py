#!/usr/bin/env python3
from utils.parse_argv import parse_argv
from utils.get_duplicates import get_info, write_duplicates


def main() -> None:
    """"""
    base_path, json_path, db_path = parse_argv()
    duplication_data, all_files_data = get_info(base_path)
    write_duplicates(json_path, duplication_data)
    write_db(db_path, all_files_data)


if __name__ == "__main__":
    main()