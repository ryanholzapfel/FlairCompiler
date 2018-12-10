"""
scanner_test.py
"""
import sys
from scanner import Scanner
sys.tracebacklimit =0

fileName = sys.argv[1]
hasFlr = ".flr"
if ".flr" in fileName:
    hasFlr = ""
fileIn = open("programs/"+ fileName + hasFlr, "r")

program = fileIn.read()

tokenList = Scanner(program)
currentToken = tokenList.next()

while True:
    print(currentToken)
    if currentToken.is_eof():
        break
    currentToken = tokenList.next()

