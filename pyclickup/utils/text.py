"""
text manipulation utilities
"""
import datetime
import re


FIRST_CAP = re.compile("(.)([A-Z][a-z]+)")
ALL_CAP = re.compile("([a-z0-9])([A-Z])")


def snakeify(text):
    """camelCase to snake_case"""
    first_string = FIRST_CAP.sub(r"\1_\2", text)
    return ALL_CAP.sub(r"\1_\2", first_string).lower()


def ts_to_datetime(timestamp):
    """converts the posix x1000 timestamp to a python datetime"""
    return datetime.datetime.utcfromtimestamp(int(timestamp) / 1000)


def datetime_to_ts(date_object):
    """converts a datetime to a posix x1000 timestamp"""
    return int(date_object.timestamp() * 1000)
