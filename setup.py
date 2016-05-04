#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ViewNudger',
    version='0.1.0',
    description="Nudges a view or object in Autodesk Maya.",
    long_description=readme,
    author="Christopher DeVito",
    author_email='chrisdevito@chribis.com',
    url='https://github.com/chrisdevito/ViewNudger',
    packages=[
        'ViewNudger',
    ],
    package_dir={'ViewNudger':
                 'ViewNudger'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='ViewNudger',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
