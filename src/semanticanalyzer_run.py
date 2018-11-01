import sys

from scanner import Scanner
from parser import Parser
# from semanticactions import *

from semanticanalyzer import SemanticAnalyzer

#bring in filepath, read program file
fileName = sys.argv[1]
file = open(fileName)
program = file.read()

#make scanner and parser objects
scanner = Scanner(program)
parser = Parser(scanner)

#parse the program and save the program node (contains all semantic actions)
programNode = parser.parse()

sa = SemanticAnalyzer(programNode)
sa.table()








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
