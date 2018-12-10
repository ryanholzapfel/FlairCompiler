"""
parse_run.py
"""

import sys
from scanner import Scanner
from parser import Parser
sys.tracebacklimit = 0


fileName = sys.argv[1]
hasFlr = ".flr"
if ".flr" in fileName:
    hasFlr = ""
fileIn = open("programs/"+ fileName + hasFlr, "r")

program = fileIn.read()



scanner = Scanner(program)
parser = Parser(scanner)

tree = parser.parse()

if tree:
    print("Program is valid.")
	#print(tree)
