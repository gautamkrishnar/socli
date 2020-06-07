# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

with open('README.rst') as f:
    longd = f.read()

setup(
    name='socli',
    include_package_data=True,
    packages=["socli"],
    entry_points = {"console_scripts": ['socli = socli.socli:main']},
    python_requires='>=3.5.0',
    install_requires=['BeautifulSoup4','requests','colorama','Py-stackExchange', 'urwid'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    requires=['BeautifulSoup4','requests','colorama','PyStackExchange', 'urwid'],
    version='4.0',
    url='http://www.github.com/gautamkrishnar/socli',
    keywords="stack overflow cli",
    license='BSD',
    author='Gautam krishna R',
    author_email='r.gautamkrishna@gmail.com',
    description='Stack overflow commnand line interface. SoCLI allows you to search and browse stack overflow from the terminal.',
    long_description="\n\n"+longd
)