import sys
import os
from codegen import CodeGen
from parser import Parser
from scanner import Scanner

def genTMFileName():
    fl = fileName.split("/")
    flairFN = fl[-1]
    flairFN = flairFN.strip(".flr")
    return flairFN



fileName = sys.argv[1]
file = open(fileName)
program = file.read()

#make scanner and parser objects
scanner = Scanner(program)
parser = Parser(scanner)

#parse the program and save the program node (contains all semantic actions)
programNode = parser.parse()
symbolTable = None
generator = CodeGen(programNode, symbolTable)
programstr = generator.generate()
fn = genTMFileName()

# cwd = os.getcwd()
# print(cwd)

tmpath = "../tm/"+ fn + ".tm"
tmOut = open(tmpath, "w")
tmOut.write(programstr)
tmOut.close()

