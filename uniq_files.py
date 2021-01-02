#!/usr/bin/env python3.9

from src.parse_argv import parse_argv
from src.storage.json_ import split_duplication_data
from src.tree import make_tree, walk_tree
from src.utils.print_ import clear_print
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
    duplications, file_stats, new_path_strs = walk_tree(root_dir, db_data)
    # Write duplication data
    if args.small_json is None:
        clear_print(f"Writing duplication JSON to {args.dup_json.path}...")
        args.dup_json.write(duplications)
    else:
        large_duplications, small_duplications = split_duplication_data(
            duplications, args.small_size
        )
        clear_print(f"Writing large duplication JSON to {args.dup_json.path}...")
        args.dup_json.write(large_duplications)
        clear_print(f"Writing small duplication JSON to {args.small_json.path}...")
        args.small_json.write(small_duplications)
    # Write all file data
    clear_print(f"Writing all file data DB to {args.db.path}...")
    args.db.write(file_stats)
    # Write new file paths
    if args.new_txt is not None:
        clear_print(f"Writing new file paths to {args.new_txt.path}")
        args.new_txt.write(new_path_strs)
    # Total time used
    print(f"Time taken: {total_time.string}")


if __name__ == "__main__":
    main()
