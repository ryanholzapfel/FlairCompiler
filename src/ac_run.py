import sys
import os
from semanticanalyzer import SemanticAnalyzer
#from codegen2 import CodeGen
from parser import Parser
from scanner import Scanner
from threeACGen import ThreeACGen

def genTMFileName():
    fl = fileName.split("/")
    flairFN = fl[-1]
    flairFN = flairFN.strip(".flr")
    return flairFN



fileName = sys.argv[1]
hasFlr = ".flr"
if ".flr" in fileName:
    hasFlr = ""
fileIn = open("programs/"+ fileName + hasFlr, "r")

flrprogram = fileIn.read()

#make scanner and parser objects
scanner = Scanner(flrprogram)
parser = Parser(scanner)



#parse the program and save the program node (contains all semantic actions)
programNode = parser.parse()
tac = ThreeACGen(programNode)
print(tac.program3AC(programNode.body().statementlist().returnstatement()))
