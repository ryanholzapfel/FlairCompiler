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


keywords = ["program","function","begin","end","return","integer","boolean","and","or","if","then","else","not","print"] 

#read file to single string
program = file.read()

#test with string of characters
#program = "program"

#load the program into the scanner object
tokenList = Scanner(program)
#get the first token
currentToken = tokenList.get_next_token()

#print tokens and get the next, break if token is EOF
while True:
    if currentToken.is_word():
        if currentToken.token_value in keywords:
            print("keyword", end=' ')
            print(currentToken.token_value)
        else:
            print(currentToken)
    elif currentToken.is_eof():
        print(currentToken)
        break
    else: #any other tokens
        print(currentToken)
    currentToken = tokenList.get_next_token()    
#print("done scanning")


