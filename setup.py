#!/usr/bin/env python
"""
pip setup file
"""
from pyclickup.globals import __version__, LIBRARY
from setuptools import setup, find_packages


with open("README.rst") as readme:
    long_description = readme.read()


setup(
    name=LIBRARY,
    version=__version__,
    description="A python wrapper for the ClickUp API",
    long_description=long_description,
    author="Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    keywords="clickup python",
    url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    download_url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    license="LICENSE",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
