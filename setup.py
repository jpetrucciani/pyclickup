#!/usr/bin/env python
"""
pip setup file
"""
from setuptools import setup, find_packages

LIBRARY = "pyclickup"


with open("README.rst") as readme:
    long_description = readme.read()


with open("requirements.txt") as requirements:
    install_requires = requirements.read().split("\n")
    install_requires = [x.strip() for x in install_requires if x.strip()]


def find_version(*file_paths):
    import os
    import re

    """
    This pattern was modeled on a method from the Python Packaging User Guide:
        https://packaging.python.org/en/latest/single_source_version.html
    We read instead of importing so we don't get import errors if our code
    imports from dependencies listed in install_requires.
    """
    base_module_file = os.path.join(*file_paths)
    with open(base_module_file) as f:
        base_module_data = f.read()
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
    long_description=long_description,
    author="Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    keywords="clickup python",
    url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    download_url="https://github.com/jpetrucciani/{}.git".format(LIBRARY),
    license="LICENSE",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
