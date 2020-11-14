#!/usr/bin/env python3
from utils.parse_argv import parse_argv
from utils.walk_directory import iter_walk


def main() -> None:
    # Parse command-line arguments
    args = parse_argv()
    # Walk directory recursively
    walker = iter_walk(args.base_path)


if __name__ == "__main__":
    main()