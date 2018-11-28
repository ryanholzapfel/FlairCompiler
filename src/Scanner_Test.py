"""
scanner_test.py
@author: Nick Rausch
"""
import sys
from scanner import Scanner

def main():

    filename = input('Enter your program name ')
    file = open("../programs/"+ filename,"r")
    print('\n')

    program = file.read()

    tokenList = Scanner(program)
    currentToken = tokenList.next_token()

    while True:
        print(currentToken)
        if currentToken.is_eof():
            break
        currentToken = tokenList.next_token()

    print('\n')
    return main()

        

if __name__ =='__main__':
    main()
