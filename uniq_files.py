#!/usr/bin/env python3.9

from src.parse_argv import parse_argv
from src.storage.json_ import split_duplication_data
from src.tree import make_tree, walk_tree
from src.utils.progress import TotalTime


def main():
    total_time = TotalTime()
    # Parse command-line arguments
    args = parse_argv()
    # Read DB
    db_data = args.db.read()
    # Get total size estimate, and make tree
    root_dir = make_tree(args.dir_path)
    # Walk through all files
    duplications, new_file_stats, removed_path_strs = walk_tree(root_dir, db_data)
    # Write duplication data
    if args.small_json is None:
        args.dup_json.write(duplications, "duplications")
    else:
        large_duplications, small_duplications = split_duplication_data(
            duplications, args.small_size
        )
        args.dup_json.write(large_duplications, "large duplications")
        args.small_json.write(small_duplications, "small duplications")
    # Write all file data
    args.db.write(new_file_stats, removed_path_strs)
    # Write new file paths
    if args.new_txt is not None:
        args.new_txt.write((file_stat.path for file_stat in new_file_stats))
    # Total time used
    print(f"Time taken: {total_time.string}")


if __name__ == "__main__":
    main()
