#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

__version__ = "0.1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENT_FILE = os.path.join(BASE_DIR, 'requirements.txt')
with open(REQUIREMENT_FILE, encoding='utf-8') as f:
    install_requires = f.readlines()

setup(
    name='coin_data',
    version=__version__,
    url='https://github.com/Jay54520/coin_data',
    description='获取各种加密货币的价格数据',
    packages=find_packages(),
    platforms='any',
    install_requires=install_requires,
)
