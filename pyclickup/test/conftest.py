"""
configure pytest
"""
import pytest
from pyclickup.test.helpers import dbg


@pytest.fixture(scope="session", autouse=True)
def before_all(request):
    """test setup"""
    dbg("[+] begin pyclickup tests")
    request.addfinalizer(after_all)


def after_all():
    """tear down"""
    dbg("[+] end pyclickup tests")
