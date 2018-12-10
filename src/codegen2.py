from semanticactions import *
from enum import Enum
from threeACGen import ThreeACGen, GenExpression
from parser import Parser
from scanner import Scanner

class CodeGen(object):
    def __init__(self, programNode, symbolTable):
        self._programNode = programNode
        self._symbolTable = symbolTable #list of lists containing all functions used in program 
        self._programName = programNode.identifier().identifier() #sting of the name of program being compiled
        self._jumpString = ['*--------- BackPatched Jumps\n'] # a string of all backpached jumps
        self._currentLine = 0 #current tm line number
        self._programString = "" # string of all tm lines in the program
        self._labelData = {} # dict of labels used in jumps
        self._jumpsToComplete = []
        self._currentLabel = 1
        self._nextOffset = 11 # this is the program arg offset that is then used as the next function offset thin number will grow in accordance to the number of args and function vars
        self._lastLiteral = []
        self._functNumber = -1
        self._ACGen = ThreeACGen
        self._temp3ACList = []
        self._functionList = []
        self._tempCode = []
        self._argOffsetList = []
        self._NumberOfProgArgs = []
        self._functionReturnOffsetDict = {}

        self.gen_table = {
            GenExpression.genSubt : self.genSubt,
            GenExpression.genAdd : self.genAdd,
            GenExpression.genDiv : self.genDiv,
            GenExpression.genCall : self.genCall,
            GenExpression.genMult : self.genMult
            }

    def currentLabel(self): # this is for when creating labels it is the next label number to be created
        tempLabel = "label" + str(self._currentLabel)
        self._currentLabel += 1
        return tempLabel  

    def currentLine(self): # gets current line for tm generation
        return self._currentLine

    def incrementLine(self): # increments line number for tm code generation
        self._currentLine += 1

    def addCode(self, code): # used to add tm code to the programString
        ln = self.currentLine()
        self._programString = self._programString + str(self.currentLine()) + ": " + code + "\n"
        self.incrementLine()

    def genKnownProgramArgs(self): # this is currently unused
        if len(self.get3AC()) == 1: #if there is only one 3AC, the program just prints a number
            treeValue = self.get3AC()[-1][2]
            self.addCode('LDC 2,{}(0) #load zero arg case'.format(treeValue))

    def initializeMain(self): # This Program Literally starts here
        self.setFunctionList() 
        self.setNumberOfProgArgs()
        programArgs = self.getNumberOfProgArgs()
        count = 1
        for arg in programArgs: # this runs once for all program args then saves them in dmem
            self.addCode('LD 2,{}(0) #load program arg {} to dmem'.format(count, arg))
            self._nextOffset += 1
            self.addCode('ST 2, {}(0) #Store cmd Line arg {} case to dmem {}'.format( self._nextOffset , arg, self._nextOffset))
            self._argOffsetList.append(self._nextOffset)
            count += 1
        self.genFunction()
        self.returnMain()
        # initiates back patching tm code generation genJump
        jumpLines = "".join(self.genJump()) #make a jump for later make sure to create jump lines last
        self._programString = self._programString + jumpLines 

    def storeReturn(self):
        #// TODO storeReturn should store return addresses acording to the function its called in
        self.addCode("LDA 1,6(7)  #load return address")
        self.addCode("ST 1,1(6)   #store return address")
        #// TODO make sure that genJump is constructing jumps proberly and often enough
        #// TODO labelData  should know what line it is so that it can jump back to the next incrementeed line properly

    def genJump(self): #generates jump stats via backpatching, label data, and jumps to complete. all jump statements must be generated last, but before return statment generation
        for jumps in self._jumpsToComplete:
            self._jumpString.append(str(jumps[0]) + ": LDA 7, {}(0)\n".format(self._labelData['label' + str(1 + self._jumpsToComplete.index(jumps))]))
        return self._jumpString
    
    def returnMain(self):# loads dmem 11 outputs it and halts program
        self.addCode("LD 2,11(0)  # load return address from dmem in imem")
        self.addCode("OUT 2,0,0   #return result of main")
        self.addCode("HALT 0,0,0  #stop execution; end of program")

    def functCount(self):#literally only keeps track of how many times genFunction is called usefull to know where in the symbol table you are
        self._functNumber += 1
        return self._functNumber

    def genFunction(self):
        #first we establish the offset in dmem for each function this will be 12 for 0 arg program 
        functionList = self.getFunctionList()
        tempFunctNumber = self.functCount() #increments for (at least) program name
        tempFunctionName = functionList[tempFunctNumber]
        if len(functionList) == 1:
            self._nextOffset += 1 
        else: # gets the number of args for a function and changes the offset to reflect that
            #//TODO  check that the offset is getting set correctly we may be accidentally changing the offset multipe times
            functionArgs = self._symbolTable[tempFunctionName][0]
            numberOfArgs = len(functionArgs)
            self._nextOffset += numberOfArgs +1
            #//TODO IMPORTANT:  need to check if theres an if statement OR print OR return
        self._programString += ("*-------------function {}\n".format(tempFunctionName)) 
        programNode = self._programNode
        tac = ThreeACGen(programNode)
        generatedACList = tac.program3AC() 
        self.set3AC(generatedACList)
        self._functionReturnOffsetDict[self._programName] = 11 # we set dmem 11 to always be the main return address
        self.genBody()

    def genBody(self):
        lastIndex = -1

        if  len(self._argOffsetList) == 0:
            # this is meant for a zero arg return case aka print-one we were working on a genPrint but never got it finished
            treeValue = self.get3AC()[-1][2]
            self.addCode('LDC 2,{}(0) #load zero arg case'.format(treeValue))
            self.addCode('ST 2, 11(0) #Store zero arg case to dmem 11') # store tree value to dmem 1 we now have our arg for 0 arg programs
            lastIndex = 0
        check3ACgenCallList = self.get3AC()
        count = -1
        for threeAC in check3ACgenCallList : #iterates through the 3ac list looking only for function calls
            count += 1
            if threeAC[0] == GenExpression.genCall:
                self.genCall(threeAC, check3ACgenCallList, count)

        while lastIndex != 0: # while last 3ac to process  
            currentOffset = self._nextOffset
            tempList = self.get3AC()
            self._temp3ACList = self.get3AC()
            temp3ACList = self._temp3ACList
            reversed3ACList = list(reversed(temp3ACList))
            for tempCode in reversed3ACList:
                tempCodeIndex = temp3ACList.index(tempCode)
                tempOperator = tempCode[0]
                if tempOperator == GenExpression.genCall:
                    lastIndex =  tempCodeIndex
                    continue 
                if tempOperator != None: # iterates through 3ac's to locate operators,
                    # then builds tm from the end of list to the first operator found repeats until it finds the beging of the 3ac list
                    if tempCode[-1] in list(self._labelData.values()):
                        for key in self._labelData.keys():
                            if self._labelData[key] == tempCode[-1] :
                                self._labelData[key] = self._currentLine
                    lastIndex =  tempCodeIndex
                    tempArg1place = tempCode[1]
                    if isinstance(tempArg1place, int):
                        tempArg1place = tempCode[1]
                        tempArg1 = temp3ACList[tempArg1place][2]
                    else:
                        for threeAC in temp3ACList:
                            if threeAC[3] == tempArg1place:
                                tempArg1 = threeAC[2]
                    if (tempCode[2].strip('t')).isalpha():
                        tempArg2place = int((self._functionReturnOffsetDict[tempCode[2]]).strip('t'))
                    else:
                        tempArg2place = int(tempCode[2].strip('t'))
                    tempArg2 = temp3ACList[tempArg2place][2]
                    self._tempCode = tempCode
                    self.getOpGen(tempOperator, tempArg1, tempArg2, tempCode[3]) #//TODO tempCode[3] is returning a wrong value in some instances needs fixing
    
        # takes a 3AC in as 3 args
    def genMult(self, tempArg1, tempArg2, tempPlace):  
        # get offset from symbol table
        functionName = self._functionList[self._functNumber] 
        offset = self._functionReturnOffsetDict[functionName]
        tPlace = int(tempPlace.strip('t'))
        if str(tempArg2).isalpha():
            arg2Offset = (self._symbolTable[functionName][0].index(tempArg2))
        if str(tempArg1).isalpha():
            arg1Offset = (self._symbolTable[functionName][0].index(tempArg1)) 
        if isinstance(offset, int):
            self.addCode("LDA 3,{}(0) # load return adress".format(offset))
        else:
            self.addCode("LDA 3,{}(0) # load return adress".format(offset.strip('t')))
        if isinstance(tempArg1,int):
            self.addCode("LDC 4,{}(0)  # load cmd line arg 1".format(tempArg1))
        else:
            self.addCode("LD 4,{}(0)  # load cmd line arg 1 or other known variable from dmem".format(1 + arg1Offset + int(str(offset).strip('t'))  ))
        if isinstance(offset,int):
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(1 + arg2Offset + offset)) # this offset should refernce a return address location in dmem
        else:
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(11 + int(str(offset).strip('t') ) ) )
        self.addCode("MUL 4,4,5   # Multiply")
        self.addCode("ST 4,11(0)  # store product in DMEM at same return address handed in")

    def genDiv(self, tempArg1, tempArg2, tempPlace):  
        # get offset from symbol table
        functionName = self._functionList[self._functNumber] 
        offset = self._functionReturnOffsetDict[functionName]
        tPlace = int(tempPlace.strip('t'))
        if str(tempArg2).isalpha():
            arg2Offset = (self._symbolTable[functionName][0].index(tempArg2))
        if str(tempArg1).isalpha():
            arg1Offset = (self._symbolTable[functionName][0].index(tempArg1)) 
        if isinstance(offset, int):
            self.addCode("LDA 3,{}(0) # load return adress".format(offset))
        else:
            self.addCode("LDA 3,{}(0) # load return adress".format(offset.strip('t')))
        if isinstance(tempArg1,int):
            self.addCode("LDC 4,{}(0)  # load cmd line arg 1".format(tempArg1))
        else:
            self.addCode("LD 4,{}(0)  # load cmd line arg 1 or other known variable from dmem".format(1 + arg1Offset + int(str(offset).strip('t'))  ))
        if isinstance(offset,int):
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(1 + arg2Offset + offset)) # this offset should refernce a return address location in dmem
        else:
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(11 + int(str(offset).strip('t') ) ) )
        self.addCode("DIV 4,4,5   # Divide")
        self.addCode("ST 4,11(0)  # store product in DMEM at same return address handed in")


    def genAdd(self, tempArg1, tempArg2, tempPlace):  
        # get offset from symbol table
        functionName = self._functionList[self._functNumber] 
        offset = self._functionReturnOffsetDict[functionName]
        tPlace = int(tempPlace.strip('t'))
        if str(tempArg2).isalpha():
            arg2Offset = (self._symbolTable[functionName][0].index(tempArg2))
        if str(tempArg1).isalpha():
            arg1Offset = (self._symbolTable[functionName][0].index(tempArg1)) 
        if isinstance(offset, int):
            self.addCode("LDA 3,{}(0) # load return adress".format(offset))
        else:
            self.addCode("LDA 3,{}(0) # load return adress".format(offset.strip('t')))
        if isinstance(tempArg1,int):
            self.addCode("LDC 4,{}(0)  # load cmd line arg 1".format(tempArg1))
        else:
            self.addCode("LD 4,{}(0)  # load cmd line arg 1 or other known variable from dmem".format(1 + arg1Offset + int(str(offset).strip('t'))  ))
        if isinstance(offset,int):
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(1 + arg2Offset + offset)) # this offset should refernce a return address location in dmem
        else:
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(11 + int(str(offset).strip('t') ) ) )
        self.addCode("ADD 4,4,5   # Add")
        self.addCode("ST 4,11(0)  # store product in DMEM at same return address handed in")

    def genSubt(self, tempArg1, tempArg2, tempPlace):
        # get offset from symbol table
        functionName = self._functionList[self._functNumber] 
        offset = self._functionReturnOffsetDict[functionName]
        tPlace = int(tempPlace.strip('t'))
        if str(tempArg2).isalpha():
            arg2Offset = (self._symbolTable[functionName][0].index(tempArg2))
        if str(tempArg1).isalpha():
            arg1Offset = (self._symbolTable[functionName][0].index(tempArg1)) 
        if isinstance(offset, int):
            self.addCode("LDA 3,{}(0) # load return adress".format(offset))
        else:
            self.addCode("LDA 3,{}(0) # load return adress".format(offset.strip('t')))
        if isinstance(tempArg1,int):
            self.addCode("LDC 4,{}(0)  # load cmd line arg 1".format(tempArg1))
        else:
            self.addCode("LD 4,{}(0)  # load cmd line arg 1 or other known variable from dmem".format(1 + arg1Offset + int(str(offset).strip('t'))  ))
        if isinstance(offset,int):
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(1 + arg2Offset + offset)) # this offset should refernce a return address location in dmem
        else:
            self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(11 + int(str(offset).strip('t') ) ) )
        self.addCode("SUB 4,4,5   # Subtract")
        self.addCode("ST 4,11(0)  # store product in DMEM at same return address handed in")

    def genCall(self,threeAC, check3ACgenCallList, count):  # //TODO this funct will likely have to be modified if we ever get time to implement if statements
        tempPlace = threeAC[3]
        #here im gonna set the 3 ac temp place to arg 1 of genCalls 3 ac then save it in a dic 
        self._functionReturnOffsetDict[threeAC[2]] = check3ACgenCallList[count + 1][3]
        tempFunctNum = self.functCount() # sets current function number for referencing it in a list and increments the next number
        thisLabel = self.currentLabel()   # sets thisLabel to the current label number and increments it by 1
        self._jumpsToComplete.append((self.currentLine() ,thisLabel, 'uncondtional' ))       
        self._labelData[thisLabel] = threeAC[1]      #jump back info                                           
        self.incrementLine()
        self._temp3ACList[count][1] = check3ACgenCallList[count + 1][3] # store an address return loction from a nested function call to the 3AC of the function that called it


    def genPrint(self, tempArg1, tempArg2, tempPlace): # is unused was supposed to handle print statements similar to a function or operator
        #self.saveReg()
        self.addCode("LDC 2,{}(0)  # load cmd line arg 1".format(tempArg1))
        self.addCode("ST 2,{}(0)  # store cmd line arg 1".format(tempPlace + self._nextOffset))
        #self.loadReg()
    
    def generate(self):     # generates all the tm codes
        self.initializeMain()
        return self._programString
#--------------------------------------------------------------------------------------getter setters

    def set3AC(self, tempList):
        self._temp3ACList = tempList
        
    def get3AC(self):
        temp = self._temp3ACList
        return temp

    def setFunctionList(self):
        fnList = [self._programName]
        for deff in self._programNode.definitions().deffs():
            fnList.append(deff.identifier().identifier())
        self._functionList =  fnList

    def getFunctionList(self):
        temp = self._functionList
        return temp

    def setNumberOfProgArgs(self):
         tempArgs = self._symbolTable[self._programName][0]
         self._NumberOfProgArgs = tempArgs

    def getNumberOfProgArgs(self):
        return self._NumberOfProgArgs

    def getOpGen(self,tempGenName, tempArg1, tempArg2, tempPlace):
        return self.gen_table[tempGenName](tempArg1, tempArg2, tempPlace)


