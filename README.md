# uniq_files

Get the duplicate files under a base path, recursively.

```text
usage: uniq_files.py [-h] -f DIR_PATH -d DB_PATH -j DUP_JSON_PATH [-b SMALL_JSON_PATH] [-n NEW_TXT_PATH] [-s SMALL_SIZE]

Check file duplicates under some base path

optional arguments:
  -h, --help            show this help message and exit
  -f DIR_PATH, --dir-path DIR_PATH
                        base directory path
  -d DB_PATH, --db-path DB_PATH
                        file database path
  -j DUP_JSON_PATH, --dup-json-path DUP_JSON_PATH
                        duplication JSON path
  -b SMALL_JSON_PATH, --small-json-path SMALL_JSON_PATH
                        small file duplication JSON path (Optional)
  -n NEW_TXT_PATH, --new-txt-path NEW_TXT_PATH
                        new file text list
  -s SMALL_SIZE, --small-size SMALL_SIZE
                        maximum file size to qualify as a small file (Default: 4 bytes)
```
