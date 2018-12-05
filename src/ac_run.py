# import sys
# import os
from semanticanalyzer import SemanticAnalyzer
#from codegen2 import CodeGen
from parser import Parser
from scanner import Scanner
from threeACGen import ThreeACGen

# def genTMFileName():
#     fl = fileName.split("/")
#     flairFN = fl[-1]
#     flairFN = flairFN.strip(".flr")
#     return flairFN




filename = input('Enter your program name ')
fileIn = open("/home/ryan/Compiler/programs/"+ filename,"r")
#fileIn = open(fileName)
flrprogram = fileIn.read()

#make scanner and parser objects
scanner = Scanner(flrprogram)
parser = Parser(scanner)



#parse the program and save the program node (contains all semantic actions)
programNode = parser.parse()
tacGen = ThreeACGen(programNode)
taclist = tacGen.program3AC(programNode.body().statementlist().returnstatement(), "t0")
for deff in programNode.definitions().deffs():
    print(taclist)
    lastID = taclist[-1][-1]
    taclist.append(tacGen.program3AC(deff.body().statementlist().returnstatement(), lastID))
print(taclist)
