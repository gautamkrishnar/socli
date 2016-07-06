try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sys import exit,version
import sys
if version < '1.0.0':
    print("Python 1 is not supported...")
    sys.exit(1)

setup(
    name='socli',
    packages=["socli"],
    entry_points = {"console_scripts": ['socli = socli.socli:main']},
    install_requires=['BeautifulSoup4','requests'],
    requires=['BeautifulSoup4','requests'],
    version='2.0',
    url='http://www.github.com/gautamkrishnar/socli',
    keywords="stack overflow cli",
    license='BSD',
    author='Gautam krishna R',
    author_email='r.gautamkrishna@gmail.com',
    description='Stack overflow commnand line interface. SoCLI allows you to search and browse stack overfow from the terninal.',
    long_description="Go to www.github.com/gautamkrishnar/socli"
    )