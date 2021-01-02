"""
Module: Byte unit conversion

Public Functions:
    byte_shorten: Shorten bytes with appropriate units
"""

from math import log2

_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]


def byte_shorten(byte_len: int) -> str:
    """
    Shorten bytes with appropriate units

    Args:
        byte_len (int): Number of bytes

    Returns:
        (str): Formatting string
    """
    if byte_len < 0:
        raise ValueError(f"Invalid number of bytes: {byte_len}")

    if byte_len < 2:
        unit_index = 0
    else:
        unit_index = int(log2(byte_len / 1.1)) // 10
        if unit_index >= len(_UNITS):
            unit_index = -1
    unit = _UNITS[unit_index]

    unit_value = 1 << (unit_index * 10)
    quotient = byte_len / unit_value

    return f"{quotient:.3f} {unit}"
