# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

with open('README.md') as f:
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
    version='5.1',
    url='https://www.github.com/gautamkrishnar/socli',
    keywords="stack overflow cli",
    license='BSD',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    author='Gautam Krishna R',
    author_email='r.gautamkrishna@gmail.com',
    description='Stack overflow command line interface. SoCLI allows you to search and browse stack overflow from the terminal.',
    long_description="\n\n"+longd,
    long_description_content_type='text/markdown'
)
