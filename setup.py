#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of configparser_extended library
# released under the MIT license.
# See the LICENSE file for more information.

import sys
from setuptools import setup, find_packages

DESCRIPTION = ("A python configparser extension")

try:
    with open('PIP.rst') as f:
        LONG_DESCRIPTION = f.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

with open('pip-requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n')
        if (line and not line.startswith('--')) and (";" not in line)
    ]

if sys.version_info[:2] < (3, 5):
    install_requires.append("configparser>=3.5.0b2")

setup(
    name='configparser_extended',
    version="0.0.1",
    author="Florian PORTUGAU, Fabien MARTY",
    author_email="florian.portugau@hotmail.fr, fabien.marty@gmail.com",
    url="https://github.com/thefab/configparser_extended",
    packages=find_packages(),
    license='MIT',
    download_url='https://github.com/thefab/configparser_extended',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
