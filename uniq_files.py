#!/usr/bin/env python3
from __future__ import annotations
from itertools import tee

from src.utils.print_funcs import clear_print
from src.argv.parse_argv import parse_argv
from src.storage.db import read_db, write_db
from src.storage.json_ import write_json, write_json_w_small
from src.directory_walker.dir_ import parse_dir
from src.file_handler.calc_size import calc_total_size
from src.file_handler.inspect_files import inspect_all_files


def main():
    """"""
    # Parse command-line arguments
    args = parse_argv()
    # Read DB
    clear_print("Reading DB...", end="")
    db_data = read_db(args.db_path)
    clear_print(f"Read {len(db_data)} entries from DB")
    # Make 2 generators
    files_gen = parse_dir(args.dir_path)
    files_gen_size, files_gen_inspect = tee(files_gen, 2)
    # Get total size estimate
    clear_print(f"Calculating total size...")
    total_size = calc_total_size(files_gen_size)
    clear_print(f"Total file size: {total_size:,}")
    # Walk through all files
    dup_list, files_props = inspect_all_files(files_gen_inspect, db_data, total_size)
    # Write JSON
    if args.small_json_path is None:
        clear_print(f"Writing JSON to {args.dup_json_path}...")
        write_json(dup_list, args.dup_json_path)
    else:
        clear_print(
            f"Writing JSON to {args.dup_json_path} and {args.small_json_path}..."
        )
        write_json_w_small(
            dup_list, args.dup_json_path, args.small_json_path, args.small_size
        )
    # Write DB
    clear_print(f"Writing DB to {args.db_path}...")
    write_db(files_props, args.db_path)


if __name__ == "__main__":
    main()