# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pruefungsplan
version = pruefungsplan.__version__

setup(
    name='pruefungsplan',
    version=version,
    author='',
    author_email='lukas@lukasklein.com',
    packages=[
        'pruefungsplan',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['pruefungsplan/manage.py'],
)