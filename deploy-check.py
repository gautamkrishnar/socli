# Python version check for travis
from sys import exit, version_info

if version_info[:2] < (3, 7):
    exit(0)
else:
    exit(1)
