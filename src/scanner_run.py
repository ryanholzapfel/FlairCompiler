"""
scanner_test.py
"""
import sys
from scanner import Scanner


fileName = sys.argv[1]
file = open(fileName)

program = file.read()

tokenList = Scanner(program)
currentToken = tokenList.next()

while True:
    print(currentToken)
    if currentToken.is_eof():
        break
    currentToken = tokenList.next()

