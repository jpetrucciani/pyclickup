"""
error models for pyclickup
"""
from typing import Any


class PyClickUpException(Exception):
    """base pyclickup exception class"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        extra = ""
        if args:
            extra = '\n| extra info: "{extra}"'.format(extra=args[0])
        print(
            "[{exception}]: {doc}{extra}".format(
                exception=self.__class__.__name__, doc=self.__doc__, extra=extra
            )
        )
        Exception.__init__(self, *args)


class RateLimited(PyClickUpException):
    """request received a 429 - you are currently rate limited"""


class MissingClient(PyClickUpException):
    """no client set for this object"""
