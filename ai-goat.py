#!/usr/bin/env python3

from sys import exit
from sys import argv
from app.menu import run


if __name__ == "__main__":
    exit(run(argv[1:]))