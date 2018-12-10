import sys

from scanner import Scanner
from parser import Parser
#sys.tracebacklimit = 0

from semanticanalyzer import SemanticAnalyzer
import os
cwd = os.getcwd()

#bring in filepath, read program file
# filename = input('Enter your program name ')
# file = open("./programs/existing_programs/"+ filename,"r")
fileName = sys.argv[1]
hasFlr = ".flr"
if ".flr" in fileName:
    hasFlr = ""
fileIn = open("programs/"+ fileName + hasFlr, "r")

program = fileIn.read()

#make scanner and parser objects
scanner = Scanner(program)
parser = Parser(scanner)

#parse the program and save the program node (contains all semantic actions)
programNode = parser.parse()

sa = SemanticAnalyzer(programNode)
print(sa.table())








# header = """Function Name |", "Function Parameters |", "Return Type","\n_______________________________________________________"""
# #mainID = programNode.identifier()
# #mainInputs = programNode.formals()

# programFunctions = []
# for function in programNode.definitions().deffs():
	# functionList = []
	# functionList.append(function.identifier())
	# functionList.append(function.formals())
	# functionList.append(function.types())
	# programFunctions.append(functionList)
	
# print(header)
# for f in programFunctions:
	# print(f[0],f[1],f[2])
