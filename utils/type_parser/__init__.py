from pathlib import Path
from typing import Callable, Dict, Generator, List, Tuple

from .zip_ import parse_zip

_DIRECTORY_EXT: Dict[
    str, Callable[[Path], Generator[Tuple[str, List[Path]], None, None]]
] = {
    ".zip": parse_zip,
}
DIRECTORY_EXT = _DIRECTORY_EXT
