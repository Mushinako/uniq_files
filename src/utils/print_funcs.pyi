from __future__ import annotations
from _typeshed import SupportsWrite
from typing import Optional


def clear_print(
    print_text: str,
    sep: Optional[str] = ...,
    end: Optional[str] = ...,
    file: Optional[SupportsWrite[str]] = ...,
    flush: bool = ...,
) -> None:
    ...


def progress_str(id_: int, count: int) -> str:
    ...


def progress_percent(finished_size: int, total_size: int) -> str:
    ...


def shrink_str(shrink: str, *, prefix: str = ..., postfix: str = ...) -> str:
    ...
