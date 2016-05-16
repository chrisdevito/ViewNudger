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


setup(
    name="ViewNudger",
    version="0.1.2",
    description="A Maya Camera or Object pixel nudger",
    long_description=readme,
    author="Christopher DeVito",
    author_email="chrisdevito@chribis.com",
    url="https://github.com/chrisdevito/ViewNudger",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["LICENSE", "README.rst", "HISTORY.rst"],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ViewNudger",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
)
