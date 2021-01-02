from _typeshed import SupportsWrite
from typing import Optional

def clear_print(
    value: str,
    *,
    sep: Optional[str] = ...,
    end: Optional[str] = ...,
    file: Optional[SupportsWrite[str]] = ...,
    flush: bool = ...,
) -> None: ...
def clear_print_clearable(
    value: str,
    *,
    sep: Optional[str] = ...,
    file: Optional[SupportsWrite[str]] = ...,
    flush: bool = ...,
) -> None: ...
def progress_str(current: int, total: int) -> str: ...
def progress_percent(current: int, total: int) -> str: ...
def shrink_str(shrink: str, *, prefix: str = ..., postfix: str = ...) -> str: ...
