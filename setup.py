#! /usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='biotools',
    version='0.1',
    packages=find_packages(),
    required_packages=['biolib'],
    author='Benjamin Fang',
    author_email='benjaminfang.ol@outlook.com',
    descrition='tools collection for bioinformatics.',
    keywords='bioinformatics tools',
    project_urls={
        'Source code':'https://github.com/benjaminfang/biotools'
    }
)
