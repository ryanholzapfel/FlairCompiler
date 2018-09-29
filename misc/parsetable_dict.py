'''
parsetable_dict.py

dict entry format
{ (NonTerminal.rule,TokenType.token_type):[NonTerminal.rule, etc. or TokenType.token_type]}
'''

import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)

tableList = []
tableDict = {}

filename = "PTread.csv"
f = open(filename)
reader = csv.reader(f)
for row in reader:
        tableList.append(row)

header = tableList[0]
"""
ruleList = []
for rule in range(1,len(tableList)):
    ruleList.append(tableList[rule][0])
"""

for r in range(1,len(tableList)):
        row = tableList[r]
#       ruleList.append(row[0])
        for c in range(1,len(row)):
                cell = row[c]
                if not (cell == ''):
                        cell = cell.strip()
                        cellList = cell.split(" ")
                        for token in cellList:
                            if token in header:
                                token = "TokenType."+token
                            else: #is a non terminal rule
                                token = "NonTerminal."+token

                        tableDict[(("NonTerminal."+row[0]), ("TokenType."+header[c]))] = cellList
                        
#print(tableDict)
pp.pprint(tableDict)    


"""
to do
--0. alter grammar rules to not include ors or left sides
1. change header to token type representation (maybe with find and replace?)
2. remove <> w/ find replace
3. 
"""
