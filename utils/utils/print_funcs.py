"""
Module: Helper functions

Public Functions:
    clear_print
"""


from _typeshed import SupportsWrite
from typing import Optional


def clear_print(
    print_text: str,
    sep: Optional[str] = None,
    end: Optional[str] = None,
    file: Optional[SupportsWrite[str]] = None,
    flush: bool = False,
) -> None:
    """
    Clear line and print
    """
    print("\r\x1b[K" + print_text, sep=sep, end=end, file=file, flush=flush)
