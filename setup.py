#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = "0.1.0"

setup(
    name='coin_data',
    version=__version__,
    url='https://github.com/Jay54520/coin_data',
    description='获取各种加密货币的价格数据',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'bitcoinaverage==0.1.15'
    ],
)
