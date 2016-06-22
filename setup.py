from setuptools import setup
from sys import exit,version
import sys
if version < '3.0.0':
    print("Python 2 is not supported...")
    sys.exit(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='socli',
    packages=["socli"],
    entry_points = {"console_scripts": ['socli = socli.socli:main']},
    version='1.0',
    url='http://www.github.com/gautamkrishnar/socli',
    keywords=['stack overflow','cli'],
    license='BSD',
    author='Gautam krishna R',
    author_email='r.gautamkrishna@gmail.com',
    description='Stack overflow commnand line interface. SoCLI allows you to search and browse stack overfow from the terninal.',
    long_description = long_descr
)