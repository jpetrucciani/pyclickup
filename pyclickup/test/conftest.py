"""
configure pytest
"""
import pytest
from pyclickup.test.helpers import dbg
from typing import Any


@pytest.fixture(scope="session", autouse=True)
def before_all(request: Any) -> None:
    """test setup"""
    dbg("[+] begin pyclickup tests")
    request.addfinalizer(after_all)


def after_all() -> None:
    """tear down"""
    dbg("[+] end pyclickup tests")
