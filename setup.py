#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyupnp',
    version='0.1',
    description='A simple UPnP library',
    author='Lars Hvile',
    author_email='lars@hulte.net',
    url='https://github.com/larshvile/pyupnp',
    packages=['pyupnp'],
    test_suite='nose.collector',
    tests_require=['nose>=1.2']
)

