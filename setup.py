# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open
from distutils.util import convert_path

with open('README.md') as f:
    longd = f.read()

main_ns = {}
ver_path = convert_path('socli/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='socli',
    include_package_data=True,
    packages=["socli"],
    entry_points={"console_scripts": ['socli = socli.sentry:main']},
    python_requires='>=3.5.0',
    install_requires=['BeautifulSoup4', 'requests', 'colorama', 'Py-stackExchange', 'sentry_sdk', 'urwid', 'argcomplete'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    requires=['BeautifulSoup4', 'requests', 'colorama', 'PyStackExchange', 'sentry_sdk', 'urwid'],
    data_files=[('man/man1',['socli.1'])],
    version=main_ns['__version__'],
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
    description='Stack overflow command line interface. SoCLI allows you to search and browse stack overflow from the '
                'terminal.',
    long_description="\n\n" + longd,
    long_description_content_type='text/markdown'
)
