"""
Module: Common errors associated with different file types

Public Classes:
    InvalidDirectoryType: Path is not a valid directory
    NotAFileError       : Operation only works on a file
"""


class InvalidDirectoryType(Exception):
    """
    Path is not a valid directory
    """

    pass


class NotAFileError(OSError):
    """
    Operation only works on a file
    """

    pass
