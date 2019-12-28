# -*- coding: utf-8 -*-
'''
setup.py: Python setuptools script + package config
'''

from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()


setup(
    name='sample',
    version='0.1.0',
    description='Code (regular expresssions and NTLK) to tokenise (remove)' + \
                ' Private Personal Information (PPI) in Python.',
    long_description=README,
    author='Lindsay Smith',
    author_email='wapdat@gmail.com',
    url='https://github.com/wapdat/ppi-sanitise',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
