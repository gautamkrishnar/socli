import sys
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path = [BASE_DIR] + sys.path
from socli import main

if __name__ == '__main__':
    main()
