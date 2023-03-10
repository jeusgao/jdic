#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Joe Gao (jeusgao@163.com)

import os
from setuptools import setup, find_packages

__version__ = '0.0.1'
requirements = open('requirements.txt').readlines()

setup(
    name = 'jdic',
    version = __version__,
    author = 'Joe_G',
    author_email = 'jeusgao@163.com',
    url = '',
    description = 'jobothub: jobot Matrix dict',
    packages = find_packages(exclude=["tests", "test", "tests.*", "test.*"]),
    python_requires = '>=3.7.0',
    install_requires = requirements,
    package_dir={'jdic':'jdic'},
    exclude_package_data={'jobothub':['.DS_Store', '*.DS_Store']},
)
