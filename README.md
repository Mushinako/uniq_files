# uniq_files

Get the duplicate files under a base path, recursively.

```text
usage: uniq_files.py [-h] -f DIR_PATH -j DUP_JSON_PATH [-b SMALL_JSON_PATH] -d DB_PATH [-s SMALL_SIZE]

Check file duplicates under some base path

optional arguments:
  -h, --help            show this help message and exit
  -f DIR_PATH, --dir-path DIR_PATH
                        Base directory path
  -j DUP_JSON_PATH, --dup-json-path DUP_JSON_PATH
                        Duplication JSON path
  -b SMALL_JSON_PATH, --small-json-path SMALL_JSON_PATH
                        Small file duplication JSON path (Optional)
  -d DB_PATH, --db-path DB_PATH
                        File database path
  -s SMALL_SIZE, --small-size SMALL_SIZE
                        Maximum file size to qualify as a small file (Default: 4 bytes)
```
