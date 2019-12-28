# -*- coding: utf-8 -*-
'''
setup.py: Python setuptools script + package config
'''
import os
import errno
import inspect
from setuptools import setup, find_packages

SETUP_PY_FILENAME = inspect.getframeinfo(inspect.currentframe()).filename
ROOT_DIR = os.path.dirname(os.path.abspath(SETUP_PY_FILENAME))
README_MD_PATH = os.path.join(ROOT_DIR, 'README.md')
README_RST_PATH = os.path.join(ROOT_DIR, 'README.rst')
README_TXT_PATH = os.path.join(ROOT_DIR, 'README.txt')
VERSION_TXT_PATH = os.path.join(ROOT_DIR, 'VERSION')

try:
    from m2r import parse_from_file
    README = parse_from_file(README_MD_PATH)
    f = open(README_RST_PATH, 'w')
    f.write(README)
    f.close()
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        try:
            os.symlink(README_RST_PATH, README_TXT_PATH)
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(README_TXT_PATH)
                os.symlink(README_RST_PATH, README_TXT_PATH)
    else:
        f = open(README_TXT_PATH, 'w')
        f.write(README)
        f.close()
except ImportError:
    # m2r may not be installed in user environment
    with open(README_MD_PATH) as f:
        README = f.read()

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [line.rstrip('\n') for line in f]

with open('LICENSE') as f:
    LICENSE = f.read()

with open(VERSION_TXT_PATH) as f:
    VERSION = f.read()

if __name__ == '__main__':
    setup(
        name='ppi-sanitize',
        version=VERSION,
        description='Code (regular expresssions and NTLK) to tokenize (remove)' + \
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
