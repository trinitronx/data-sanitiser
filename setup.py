# -*- coding: utf-8 -*-
'''
setup.py: Python setuptools script + package config
'''
import os
from setuptools import setup, find_packages

VERSION_TXT_PATH  = os.path.join(ROOT_DIR, 'VERSION')

with open('README.md') as f:
    README = f.read()

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [line.rstrip('\n') for line in f]
    print(INSTALL_REQUIRES)

with open('LICENSE') as f:
    LICENSE = f.read()

with open(VERSION_TXT_PATH) as f:
    VERSION = f.read()

if __name__ == '__main__':
    setup(
        name='ppi-sanitise',
        version=VERSION,
        description='Code (regular expresssions and NTLK) to tokenise (remove)' + \
                    ' Private Personal Information (PPI) in Python.',
        long_description=README,
        author='Lindsay Smith',
        author_email='wapdat@gmail.com',
        url='https://github.com/wapdat/ppi-sanitise',
        license=LICENSE,
        packages=find_packages(exclude=('tests', 'docs')),
        install_requires=INSTALL_REQUIRES,
        test_suite="nose2.collector.collector",
        tests_require="nose2~=0.9"
    )
