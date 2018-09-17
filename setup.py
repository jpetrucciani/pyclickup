#!/usr/bin/env python
"""
pip setup file
"""
from pyclickup.globals import __version__, LIBRARY
from setuptools import setup


setup(
    name=LIBRARY,
    version=__version__,
    description=("A python wrapper for the ClickUp API"),
    author="Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    download_url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    license="LICENSE",
    packages=[LIBRARY, "{}.models".format(LIBRARY)],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
