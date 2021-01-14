# uniq_files

Get the duplicate files under a base path, recursively.

```text
usage: uniq_files.py [-h] -f DIR_PATH -d DB [-t NEW_TXT] [-e EMPTY_TXT] -j DUP_JSON [-js SMALL_JSON] [-jl LARGE_JSON] [-s SMALL_SIZE] [-l LARGE_SIZE]

check file duplicates under some base path

optional arguments:
  -h, --help            show this help message and exit

inputs:
  -f DIR_PATH, --dir-path DIR_PATH
                        base directory path

outputs:
  -d DB, --db-path DB   file database path
  -t NEW_TXT, --new-txt-path NEW_TXT
                        new files list text path (Optional)
  -e EMPTY_TXT, --empty-txt-path EMPTY_TXT
                        empty directories list text path (Optional)

JSON outputs:
  -j DUP_JSON, --dup-json-path DUP_JSON
                        duplication JSON path
  -js SMALL_JSON, --small-json-path SMALL_JSON
                        small file duplication JSON path (Optional)
  -jl LARGE_JSON, --large-json-path LARGE_JSON
                        large file duplication JSON path (Optional)

configs:
  -s SMALL_SIZE, --small-size SMALL_SIZE
                        maximum file size to qualify as a small file (Default: 1,024 bytes)
  -l LARGE_SIZE, --large-size LARGE_SIZE
                        minimum file size to qualify as a large file (Default: 536,870,912 bytes)
```
