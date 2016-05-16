#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages

if sys.argv[-1] == "pypi":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

import ViewNudger

setup(
    name=ViewNudger.__title__,
    version=ViewNudger.__version__,
    description=ViewNudger.__description__,
    long_description=readme,
    author=ViewNudger.__author__,
    author_email=ViewNudger.__email__,
    url=ViewNudger.__url__,
    license=ViewNudger.__license__,
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["LICENSE", "README.rst", "HISTORY.rst"],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=ViewNudger.__title__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
)
