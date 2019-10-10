#!/usr/bin/env python
"""
pip setup file
"""
from setuptools import setup, find_packages


LIBRARY = "pyclickup"


with open("README.md") as readme:
    LONG_DESCRIPTION = readme.read()


with open("requirements.txt") as requirements:
    INSTALL_REQUIRES = requirements.read().split("\n")
    INSTALL_REQUIRES = [x.strip() for x in INSTALL_REQUIRES if x.strip()]


def find_version(*file_paths):
    """
    This pattern was modeled on a method from the Python Packaging User Guide:
        https://packaging.python.org/en/latest/single_source_version.html
    We read instead of importing so we don't get import errors if our code
    imports from dependencies listed in install_requires.
    """
    import os
    import re

    base_module_file = os.path.join(*file_paths)
    with open(base_module_file) as file:
        base_module_data = file.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", base_module_data, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name=LIBRARY,
    version=find_version("pyclickup", "globals.py"),
    description="A python wrapper for the ClickUp API",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    keywords="clickup python",
    url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    download_url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    license="LICENSE",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe=False,
)
