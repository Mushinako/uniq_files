#!/usr/bin/env python3
from __future__ import annotations
from itertools import tee

from src.utils.print_funcs import clear_print
from src.argv.parse_argv import parse_argv
from src.storage.db import read_db, write_db
from src.directory_walker.dir_ import parse_dir


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
    files_gen1, files_gen2 = tee(files_gen)
    # Get total size estimate


if __name__ == "__main__":
    main()