from os import sep as os_sep
from re import compile as re_compile, Pattern
from json import load as json_load
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.json"


@dataclass
class Whitelist:
    """"""

    dir_names: Set[str]
    dir_paths: Set[str]
    file_names: Set[str]
    file_paths: Set[str]
    file_regexes: Set[Pattern]


@dataclass
class Config:
    """"""

    whitelist: Whitelist


def get_config() -> Config:
    """"""
    with open(CONFIG_FILE, "r") as config_fp:
        config = json_load(config_fp)

    whitelists: Dict[str, List[str]] = config["whitelists"]
    whitelisted_dirnames = set(whitelists["dirnames"])
    whitelisted_dirpaths = set(Path(path) for path in whitelists["dirpaths"])
    whitelisted_filenames = set(whitelists["filenames"])
    whitelisted_filepaths = set(Path(path) for path in whitelists["filepaths"])
    whitelisted_fileregexes = set(
        re_compile(r.replace("{sep}", os_sep)) for r in whitelists["fileregexes"]
    )
    whitelist_obj = Whitelist(
        whitelisted_dirnames,
        whitelisted_dirpaths,
        whitelisted_filenames,
        whitelisted_filepaths,
        whitelisted_fileregexes,
    )

    config = Config(whitelist_obj)
    return config


CONFIG = get_config()


def progress_str(id_: int, count: int) -> str:
    """"""
    count_str = str(count)
    return f"{str(id_).rjust(len(count_str))}/{count_str}"
