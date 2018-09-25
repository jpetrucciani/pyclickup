"""
text manipulation utilities
"""
import re
from datetime import datetime
from typing import Any


FIRST_CAP = re.compile("(.)([A-Z][a-z]+)")
ALL_CAP = re.compile("([a-z0-9])([A-Z])")
LOCALS_FILTER = ["self", "kwargs"]


def snakeify(text: str) -> str:
    """camelCase to snake_case"""
    first_string = FIRST_CAP.sub(r"\1_\2", text)
    return ALL_CAP.sub(r"\1_\2", first_string).lower()


def ts_to_datetime(timestamp: int) -> datetime:
    """converts the posix x1000 timestamp to a python datetime"""
    return datetime.utcfromtimestamp(int(timestamp) / 1000)


def datetime_to_ts(date_object: datetime) -> int:
    """converts a datetime to a posix x1000 timestamp"""
    return int(date_object.timestamp() * 1000)


def filter_locals(local_variables: Any, extras: list = None) -> dict:
    """filters out builtin variables in the local scope and returns locals as a dict"""
    var_filter = LOCALS_FILTER.copy()
    if extras and isinstance(extras, list):
        var_filter += extras
    return {
        x: local_variables[x]
        for x in local_variables
        if local_variables[x] is not None and x not in var_filter
    }
