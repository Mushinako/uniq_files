#!/usr/bin/env python3
from __future__ import annotations
from time import time
from itertools import tee

from src.utils.print_funcs import clear_print
from src.parse_argv import parse_argv
from src.storage.db import read_db, write_db
from src.storage.json_ import write_json, write_json_w_small
from src.directory_walker.dir_ import parse_dir
from src.file_handler.calc_size import calc_total_size
from src.file_handler.inspect_files import inspect_all_files
from src.storage.txt import write_txt
from src.utils.parse_time import parse_time


def main():
    """"""
    start = time()
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
    dup_list, files_props, new_files = inspect_all_files(
        files_gen_inspect, db_data, total_size
    )
    # Write JSON
    if args.small_json_path is None:
        clear_print(f"Writing duplication JSON to {args.dup_json_path}...")
        write_json(dup_list, args.dup_json_path)
    else:
        clear_print(
            f"Writing duplication JSON to {args.dup_json_path} and {args.small_json_path}..."
        )
        write_json_w_small(
            dup_list, args.dup_json_path, args.small_json_path, args.small_size
        )
    # Write DB
    clear_print(f"Writing all file data DB to {args.db_path}...")
    write_db(files_props, args.db_path)
    # Write text
    if args.new_txt_path is not None:
        clear_print(f"Writing new file paths to {args.new_txt_path}")
        write_txt(new_files, args.new_txt_path)
    # Total time used
    duration = time() - start
    print(f"Time taken: {parse_time(duration)}")


if __name__ == "__main__":
    main()