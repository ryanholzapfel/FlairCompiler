

"""
scanner_test.py
"""
import sys
from scanner import Scanner
from parser import Parser

def main():

    filename = input('Enter your program name ')
    file = open("../programs/"+ filename,"r")
    print('\n')

    program = file.read()
    scanner - Scanner(program)
    parser = Parser(scanner)
    
    valid = parser.parse()
    
    if valid:
        print('Program is valid')

    print('\n')
    return main()

        

if __name__ =='__main__':
    main()
