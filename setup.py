#!/usr/bin/env python
"""
pip setup file
"""
from setuptools import setup, find_packages


__library__ = "pyclickup"
__version__ = "VERSION"

__user__ = "https://github.com/jpetrucciani"


with open("README.md") as readme:
    LONG_DESCRIPTION = readme.read()


with open("requirements.txt") as requirements:
    INSTALL_REQUIRES = requirements.read().split("\n")
    INSTALL_REQUIRES = [x.strip() for x in INSTALL_REQUIRES if x.strip()]


setup(
    name=__library__,
    version=__version__,
    description="A python wrapper for the ClickUp API",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Jacobi Petrucciani",
    author_email="j@cobi.dev",
    keywords="clickup python",
    url=f"{__user__}/{__library__}.git",
    download_url=f"{__user__}/{__library__}.git",
    license="LICENSE",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe=False,
)
