"""
Module: Helper functions

Public Functions:
    clear_print
"""


def clear_print(print_text: str, **kwargs) -> None:
    """
    Clear line and print
    """
    print("\r\x1b[K" + print_text, **kwargs)
