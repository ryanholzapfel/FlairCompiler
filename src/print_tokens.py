from scanner import Scanner
from flair_tokens import Token, TokenType
import sys


'''
print_tokens.py
Uses the Flair scanner to make a human-readable
list of tokens in a Flair program

'''


#file name and open
fileName = sys.argv[1]
file = open(fileName)




#read file to single string
program = file.read()

#program = "program"

#load the program into the scanner object
tokenList = Scanner(program)
#get the first token
currentToken = tokenList.get_next_token()
#print tokens and get the next, break if token is EOF
while True:
    print(currentToken)
    if currentToken.is_eof():
        break
    currentToken = tokenList.get_next_token()
    
print("done scanning")


