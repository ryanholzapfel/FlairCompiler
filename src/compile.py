import sys
import os
from semanticanalyzer import SemanticAnalyzer
from codegen2 import CodeGen
from parser import Parser
from scanner import Scanner

def genTMFileName():
    fl = fileName.split("/")
    flairFN = fl[-1]
    flairFN = flairFN.split(".")
    return flairFN[0]

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
sa = SemanticAnalyzer(programNode)
symbolTable = sa.table()
generator = CodeGen(programNode, symbolTable)
tmprogramstr = generator.generate()
fn = genTMFileName()
tmpath = "./tm/"+ fn + ".tm"
tmOut = open(tmpath, "w")
tmOut.write(tmprogramstr)
tmOut.close()

