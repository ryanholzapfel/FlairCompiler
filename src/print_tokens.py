from scanner import Scanner
from flair_tokens import Token, TokenType
'''
#file in
fileName = argv[1]

file = open(fileName)
'''

program = "program(a : int) end"

#file to line

#program = file.read()
tokenList = Scanner(program)
currentToken = tokenList.getNextToken()
while currentToken.TokenType() not EOF:
    

print("done scanning")
print(tokenList)

