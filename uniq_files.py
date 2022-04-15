#!/usr/bin/env python3.10

from src.data.file_stat import FileStat
from src.parse_argv import parse_argv
from src.storage.yaml_ import write_dup
from src.tree import make_tree, walk_tree
from src.utils.progress import TotalTime


def main():
    total_time = TotalTime()

    # Parse command-line arguments
    args = parse_argv()
    # Read DB
    db_data: dict[str, FileStat] = {} if args.db is None else args.db.read()

    # Get total size estimate, and make tree
    root_dir = make_tree(args.dir_path)
    # Walk through all files
    (
        duplications,
        new_file_stats,
        removed_path_strs,
        empty_dirs,
    ) = walk_tree(root_dir, db_data)

    # Write all file data
    if args.db is not None:
        args.db.write(new_file_stats, removed_path_strs)
    # Write new file paths
    if args.new_txt is not None:
        args.new_txt.write(
            (file_stat.path for file_stat in new_file_stats), "new file paths"
        )
    # Write empty directory paths
    if args.empty_txt is not None:
        args.empty_txt.write(empty_dirs, "empty directory paths")

    # Write duplication data
    write_dup(
        duplications,
        args.dup_yaml,
        small_yaml=args.small_yaml,
        large_yaml=args.large_yaml,
        small_size=args.small_size,
        large_size=args.large_size,
    )

    # Total time used
    print(f"Time taken: {total_time.string}")


if __name__ == "__main__":
    main()
