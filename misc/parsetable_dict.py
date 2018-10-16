'''
parsetable_dict.py

dict entry format
{ (NonTerminal.rule,TokenType.token_type):[NonTerminal.rule, etc. or TokenType.token_type]}
'''

'''
COMMAND LINE USAGE: python3 parsetable_dict.py > FILENAME
'''

import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)

tableList = []
tableDict = {}


#change filename if applicable
filename = "pt1016-2.csv"


f = open(filename)
reader = csv.reader(f)
for row in reader:
        tableList.append(row)

#List of TokenType (Terminal Tokens)
header = tableList[0]
"""
ruleList = []
for rule in range(1,len(tableList)):
    ruleList.append(tableList[rule][0])
"""

#for each row in the table
for r in range(1,len(tableList)):
        row = tableList[r]
#       ruleList.append(row[0])
        #for each cell/item in the row
        for c in range(1,len(row)):
                cell = row[c]
                #if the cell has rules in it
                if not (cell == ''):
                        #strip whitespace from ends, split on interior spaces
                        cell = cell.strip()
                        cellList = cell.split(" ")
                        #for token/rule in the cell, check if its a terminal/non-terminal, format for parse_dict
                        for token in range(0,len(cellList)):
                            cellList[token] = cellList[token].strip()
                            if cellList[token] in header:
                                cellList[token] = "TokenType."+cellList[token]
                            elif "_" in cellList[token]:
                                cellList[token] = "Ast_Type."+cellList[token]
                            else: #is a non terminal rule
                                cellList[token] = "NonTerminal."+cellList[token]
                           # print(token)


                        #create parse_dict entry

                        tableDict[(("NonTerminal."+row[0]), ("TokenType."+header[c]))] = cellList
                        
#print(tableDict)
pp.pprint(tableDict)    

#load output file in a text editor, find/replace all single quotes with empty string
#find/replace all NonTerminal.epsilon with empty string
#copy paste into parser
