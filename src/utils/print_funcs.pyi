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
