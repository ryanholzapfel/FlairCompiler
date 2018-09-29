
"""
parse_run.py
"""

import sys
from scanner import Scanner
from parser import Parser


fileName = sys.argv[1]

file = open(fileName)

program = file.read()

scanner = Scanner(program)
parser = Parser(program)

print(parser)
