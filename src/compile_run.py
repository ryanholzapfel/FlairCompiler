import sys
import os
import pwd
from codegen2 import CodeGen
from parser import Parser
from scanner import Scanner
from semanticanalyzer import SemanticAnalyzer

def genTMFileName():
    fl = filename.split("/")
    flairFN = fl[-1]
    flairFN = flairFN.strip(".flr")
    return flairFN
    #return "print-one"


user = pwd.getpwuid(os.getuid()).pw_name
filename = input('Enter your program name ')
fileIn = open("/home/"+ user +"/Compiler/programs/"+ filename,"r")
#fileIn = open(fileName)
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

#cwd = os.getcwd()
#print(cwd)
#print(programstr)

tmpath = "./tm/"+ fn + ".tm"
tmOut = open(tmpath, "w")
tmOut.write(tmprogramstr)
tmOut.close()

