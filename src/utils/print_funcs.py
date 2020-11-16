"""
Module: Helper functions

Public Functions:
    clear_print
"""
from __future__ import annotations
from typing import Any, Optional


def clear_print(
    print_text: str,
    sep: Optional[str] = None,
    end: Optional[str] = None,
    file: Optional[Any] = None,
    flush: bool = False,
) -> None:
    """
    Clear line and print
    """
    print("\r\x1b[K" + print_text, sep=sep, end=end, file=file, flush=flush)
