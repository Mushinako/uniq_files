#!/usr/bin/env python3
from utils.parse_argv import parse_argv
from utils.db import read_database, write_database
from utils.walk_directory import iter_walk, iter_walk_size
from utils.inspect_file import check_files
from utils.json_ import write_json


def main() -> None:
    # Parse command-line arguments
    args = parse_argv()
    # Read DB
    print("Reading DB...")
    files_data = read_database(args.file_database_path)
    # Walk directory recursively
    print("Calculating size...")
    total_size = iter_walk_size(args.base_path)
    walker = iter_walk(args.base_path)
    output_json_list, all_files = check_files(walker, files_data, total_size)
    # Write JSON
    print("Writing JSON...")
    write_json(args.dup_json_path, output_json_list)
    # Write DB
    print("Writing DB...")
    write_database(args.file_database_path, all_files)


if __name__ == "__main__":
    main()