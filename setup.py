# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open
from sys import exit,version
import sys
if version < '1.0.0':
    print("Python 1 is not supported...")
    sys.exit(1)

with open('README.rst') as f:
    longd = f.read()

setup(
    name='socli',
    packages=["socli"],
    entry_points = {"console_scripts": ['socli = socli.socli:main']},
    install_requires=['BeautifulSoup4','requests','colorama','Py-stackExchange'],
    requires=['BeautifulSoup4','requests','colorama','PyStackExchange'],
    version='3.4',
    url='http://www.github.com/gautamkrishnar/socli',
    keywords="stack overflow cli",
    license='BSD',
    author='Gautam krishna R',
    author_email='r.gautamkrishna@gmail.com',
    description='Stack overflow commnand line interface. SoCLI allows you to search and browse stack overflow from the terminal.',
    long_description="\n\n"+longd
    )
