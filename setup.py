#!/usr/bin/env python3
import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = ""

setup(
    name='ImageHash',
    version="0.0.1",
    author='Patrik Pettersson',
    author_email='pettersson.pa@gmail.com',
    packages=['pyioc'],
    scripts=['find_similar_images.py'],
    url='https://github.com/kaffepanna/pyioc',
    license='BSD 2-clause (see LICENSE file)',
    description='Python dependency injection',
    long_description=long_description,
    install_requires=[
        "pyyaml",
    ],
    test_suite='tests'
)
