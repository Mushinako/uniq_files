#!/usr/bin/env python3
from __future__ import annotations
from itertools import tee

from src.utils.print_funcs import clear_print
from src.argv.parse_argv import parse_argv
from src.storage.db import read_db, write_db
from src.directory_walker.dir_ import parse_dir
from src.file_handler.calc_size import calc_total_size


def main():
    """"""
    # Parse command-line arguments
    args = parse_argv()
    # Read DB
    clear_print("Reading DB...", end="")
    db_data = read_db(args.db_path)
    clear_print(f"Read {len(db_data)} entries from DB")
    # Make 2 generators
    files_gen = parse_dir(args.base_path)
    files_gen_size, files_gen_inspect = tee(files_gen, n=2)
    # Get total size estimate
    clear_print(f"Calculating total size...")
    total_size = calc_total_size(files_gen_size)
    clear_print(f"Total file size: {total_size:,}")
    # Walk through all files


if __name__ == "__main__":
    main()