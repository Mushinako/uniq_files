#!/usr/bin/env python3
from __future__ import annotations

from utils.utils.print_funcs import clear_print
from utils.argv.parse_argv import parse_argv
from utils.storage.db import read_db, write_db


def main():
    """"""
    # Parse command-line arguments
    args = parse_argv()
    # Read DB
    clear_print("Reading DB...", end="")
    db_data = read_db(args.db_path)
    clear_print(f"Read {len(db_data)} entries from DB")
    # Get total size estimate


if __name__ == "__main__":
    main()