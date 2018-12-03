from semanticactions import *
from enum import Enum
from threeACGen import ThreeACGen, GenExpression
from parser import Parser
from scanner import Scanner


# class GenExpression(Enum):
#     genMult     = 1
#     genDiv      = 2
#     genAdd      = 3
#     genSubt     = 4
#     genLess     = 5
#     genEqual    = 6
#     genOr       = 7
#     genIf       = 8
#     genAnd      = 9
#     genNot      = 10
#     genNeg      = 11
#     genPrint    = 12
#     genReturn   = 13
#     genBool     = 14

# gen_table = {
#         GenExpression.genMult : genMult
# }




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
        self._availableIMEM = ["locked",0,0,0,0,1,1,"locked"] #locked = reserved (PC and const. 0), 0= not in use, 1= in use
        self._currentLabel = 1
        self._nextOffset = 11 # this is the program arg offset that is then used as the next function offset thin number will grow in accordance to the number of args and function vars
        self._lastLiteral = []
        self._functNumber = -1
        self._ACGen = ThreeACGen
        self._temp3ACList = []
        self._functionList = []
        self._tempCode = []
        
        self._offsetList = []




    def toggleIMEM(self, regNum):
        if self._availableIMEM[regNum] == 0:
            self._availableIMEM[regNum] = 1
        elif self._availableIMEM[regNum] == 1:
            self._availableIMEM[regNum] = 0

    def currentLabel(self): # this is for when creating labels it is the next label number to be created
        tempLabel = "label" + str(self._currentLabel)
        self._currentLabel += 1
        return tempLabel  

    def regInUse(self, regNum):# used to toggle available imem register as in use
        self._availableIMEM[regNum] = 1
    
    def regAvail(self, regNum):#  used to toggle in use imem register as available
        self._availableIMEM[regNum] = 0

    def getRegister(self):
        try: 
            return self._availableIMEM.index(0)
        except ValueError:
            regToMove = self._availableIMEM.index(1)
            self.addCode("ST {},{}(0)  #move register {} to DMEM{}".format(regToMove,regToMove,regToMove,regToMove))
            self._availableIMEM[regToMove] = 0
            return regToMove
    
    def currentLine(self):
        return self._currentLine

    def incrementLine(self):
        self._currentLine += 1

    def addCode(self, code):
        ln = self.currentLine()
        self._programString = self._programString + str(self.currentLine()) + ": " + code + "\n"
        self.incrementLine()

    def genPointers(self):
        self.addCode("LDC 5,-1(0)  #initialize status ptr")
        self.addCode("LDC 6,2(0)   #initialize top ptr")

    def savePointers(self):
        pass
    
    def genProgramArgs(self):
        #progArgs= self._symbolTable[self._programName]
        #for arg in progArgs: # how i get the arg here is wrong i for got where the args are passed in possibly in the tree???
        #    tempReg = getRegister()
        #    self.addCode("LDC {},{}(0)  #load arg".format(tempReg, arg))#need to save command line arg here 
        #    self.addCode('ST {},{}(11) #save arg to dmem'.format(tempReg, arg.index())) # to find arg in dmem use the index in symboyl table of arg desired plus an offset of 11
            #IMPORTANT: we should set up an offset in case there are more than 3 args passed in. which is highly probable
            #IMPORTANT: if we decide to store function variables in dmem we need to count keep track of all args and previous variables saved in dmem 
            #  or we risk overwriting important dmem registers

        #IMPORTANT: we still need to handle 0 arg cases we can do this by looking at the bottom of the program node to see what value is returned, 
        # then load that as our arg, this will probably only be useful in print one style cases we only do this if symbol table has 0 args
        #treeValue = self._programNode.body().statementlist().returnstatement().sexpr().term().factor().literal() #will this work for any zero arg case????
        # if isinstance(temp_arg, Integer_Node):
        #     treeValue = self._programNode.body().statementlist().returnstatement().sexpr().term().factor().literal().integer()
        # else:
        #     treeValue = self._programNode.body().statementlist().returnstatement().sexpr().term().factor().literal().boolean()
        #if len(self._symbolTable[self._programName][0]) == 0:
        if len(self.get3AC()) == 1: #if there is only one 3AC, the program just prints a number
            #treeValue = self._programNode.body().statementlist().returnstatement().sexpr().term().factor().literal()
            treeValue = self.get3AC()[-1][2]
            self.addCode('LDC 2,{}(0) #load zero arg case'.format(treeValue))
            self.addCode('ST 2, 1(0) #Store zero arg case to dmem 1') # store tree value to dmem 1 we now have our arg for 0 arg programs

            # would look like --> self.addCode("LDC {},{}({})  #load arg".format(getRegister(), <arg>, <offset>)) where offset is determinde either by the number of args in symbol table or set at a constant 10
            #might have to keep track of how mnay times getRegister is called 

            # i dont toggle the registers here because i save the args to dmem. if we choose to optimize we can toggle registers especially if there 
            # are 3 args or less so that we dont have to reload them later in the secuence. it would likely help by reducing stack size

    def genTMProgram(self):
        self.initializeMain()
        

    def saveReg(self): # typically used to store imem before a function call to save current state of main prog stored from dmem 6-10
        self.addCode("ST 0,1(5)   #save IMEM to DMEM")
        self.addCode("ST 1,2(5)   #save IMEM to DMEM")
        self.addCode("ST 2,3(5)   #save IMEM to DMEM")
        self.addCode("ST 3,4(5)   #save IMEM to DMEM")
        self.addCode("ST 4,5(5)   #save IMEM to DMEM")

    def loadReg(self): # used after a funtion calll to return imem to previous main prog state
        self.addCode("LD 0,1(5)   #load DMEM to IMEM")
        self.addCode("LD 1,2(5)   #load DMEM to IMEM")
        self.addCode("LD 2,3(5)   #load DMEM to IMEM")
        self.addCode("LD 3,4(5)   #load DMEM to IMEM")
        self.addCode("LD 4,5(5)   #load DMEM to IMEM")

    def initializeMain(self): # This Program Literally starts here
        self.genPointers()
        self.storeReturn()
        self.setFunctionList()

        
        self.genFunction()

        thisLabel = self.currentLabel()                                                  # this should be factored out                           
        self._jumpsToComplete.append((self.currentLine() ,thisLabel, 'uncondtional' ))   # this should be factored out       
        self._labelData[thisLabel] = self.currentLine() + 1                              # this should be factored out                       
        self.incrementLine()                                                             # this should be factored out
        self.returnMain()
        jumpLines = "".join(self.genJump()) #make a jump for later make sure to create jump lines last
        
        self._programString = self._programString + jumpLines

    def storeReturn(self):
        self.addCode("LDA 1,6(7)  #load return address")
        self.addCode("ST 1,1(6)   #store return address")

    def genJump(self): #generates jump stats via backpatching, label data, and jumps to complete. all jump statements must be generated last, but before return statment generation
        for jumps in self._jumpsToComplete:
            self._jumpString.append(str(jumps[0]) + ": LDA 7, {}(0)\n".format(self._labelData['label' + str(1 + self._jumpsToComplete.index(jumps))]))
        return self._jumpString
    
    def returnMain(self):#wip previously worked as ("LDC 2, 1 (0)" #literal one)
        #hardcode literal 1
        #self.addCode("LDC 2,1(0)  #literal one")
        #end hardcode
        self.genProgramArgs()
        #not hardcoded WIP
        #self.addCode("LDC 2,{}(0)  #literal one".format(commandArg))#need to save command line arg here
        #
        
        self.addCode("OUT 2,0,0   #return result of main")
        self.addCode("HALT 0,0,0  #stop execution; end of program")

    def functCount(self):#literally only keeps track of how many times genFunction is called usefull to know where in the symbol table you are
        self._functNumber += 1
        return self._functNumber

    def genFunction(self):
        #first we establish the offset in dmem for each function this will be 12 for a 1 or 0 arg program to a finite number no more than 1000
        functionList = self.getFunctionList()
        self._offsetList.append(self._nextOffset)
        tempFunctNumber = self.functCount()
        tempFunctionName = functionList[tempFunctNumber]
        if len(functionList) == 1:
            self._nextOffset += 2 # +2 might cauz issues ttry +1

        else:
            self._nextOffset
            functionArgs = self._symbolTable[tempFunctionName][0]
            numberOfArgs = len(functionArgs)
            self._nextOffset += numberOfArgs +1

            # begining of the function in the tm code
        
            #IMPORTANT: may need to check if theres an if statement
            # OR print 
            # OR return
            # i think the symbol table needs to be modified to include these not sure
        self._programString += ("*-------------function {}\n".format(tempFunctionName)) # replaced functName with functNumber because i messed up call to find name in line 173

        programNode = self._programNode
        tac = ThreeACGen(programNode)
        generatedACList = tac.program3AC(programNode.body().statementlist().returnstatement())
        print(generatedACList)
        self.set3AC(generatedACList)

        

        self.genBody()

    # table to access generating functuons for tm code

    # def getOp(self):
    #     tempCode = self._temp3ACList.pop()
    #     #print(tempCode)
    #     tempOperator = tempCode[0]
    #     #print(tempCode[0])

    #     if tempOperator == None:
    #         self.getOp()
    #     else:
    #         return tempCode[0]

    # def getArg1(self):
    #     tempCode = self._temp3ACList.pop()

    #     tempArg = tempCode[2]

    #     if tempArg == None:
    #         self.getArg1()

    #     return tempArg

    # def getArg2(self):
    #     tempCode = self._temp3ACList.pop()

    #     tempArg = tempCode[2]

    #     if tempArg == None:
    #         self.getArg2()

    #     return tempArg
            

    def genBody(self):
        lastIndex = -1
        if len(self.get3AC()) == 1:
            treeValue = self.get3AC()[-1][2]
            self.addCode('LDC 2,{}(0) #load zero arg case'.format(treeValue))
            self.addCode('ST 2, 1(0) #Store zero arg case to dmem 1') # store tree value to dmem 1 we now have our arg for 0 arg programs
            lastIndex = 0





        
        while lastIndex != 0:
        
            #maybe move out of while loop?
            currentOffset = self._nextOffset
            tempList = self.get3AC()
            
            
            
            self._temp3ACList = self.get3AC()
            print(" should be the full 3 ac list from opererator" )
            print(self.get3AC())
            temp3ACList = self._temp3ACList
            
            reversed3ACList = list(reversed(temp3ACList))
            print(reversed3ACList)

            for tempCode in reversed3ACList:
                tempCodeIndex = temp3ACList.index(tempCode)
                #tempCode = reversed3ACList[tempCodeIndex]
                tempOperator = tempCode[0]
                print('inside for loop')
                print(tempCode)
                if tempOperator != None:
                    print('tempOP')
                    print(tempOperator)
                    lastIndex =  tempCodeIndex

                    tempArg1place = int(tempCode[1].strip('t'))
                    tempArg2place = int(tempCode[2].strip('t'))
                    print('this is arg 2')
                    print(tempArg2place)

                    tempArg1 = temp3ACList[tempArg1place][2]
                    tempArg2 = temp3ACList[tempArg2place][2]
                    #threeACCode =[tempOperator,tempArg1, tempArg2, tempCode[3]]
                    self._tempCode = tempCode
                    print('self._temp inside of for loop inside if state')
                    print(self._tempCode)
                    #genTemp = gen_table.get(tempOperator)
                    print('3ac values arg1 arg2 tempPlace')
                    print(tempArg1, tempArg2, tempCode[3])
                    self.genMult(tempArg1, tempArg2, tempCode[3])

                    #genOperator(threeACCode)
                    

                # self._temp3ACList = self.get3AC()
            
                # print(" should be the full 3 ac list from arg 1" )
                # print(self.get3AC())
                # print(self._tempCode)
           
                # tempPlaceArg1 = int(tempCode[1].strip('t'))
                # temp3ACList = self.get3AC()



                # tempCode = self._temp3ACList.pop()
                # tempArg1 = tempCode[2]
                # while tempArg1 == None:
                #     tempCode = self._temp3ACList.pop()
                #     tempArg1 = tempCode[2]

                # self._temp3ACList = self.get3AC()
                # tempCode = self._temp3ACList.pop()
                # tempArg1 = tempCode[2]
                # while tempArg2 == None:
                #     tempCode = self._temp3ACList.pop()
                #     tempArg2 = tempCode[2]

    
        
    def genMult(self, tempArg1, tempArg2, tempPlace): #r2 is possibly not zero a,b,c is possibly t1,t2,t3
        # get offset from symbol table
        offset = self._offsetList[self._functNumber]
        functionName = self._functionList[self._functNumber]
        tPlace = int(tempPlace.strip('t'))
        if str(tempArg2).isalpha():
            arg2Offset = self._symbolTable[functionName][0].index(tempArg2)
        if str(tempArg1).isalpha():
            arg1Offset = self._symbolTable[functionName][0].index(tempArg1)
            
        self.saveReg()
        self.addCode("LDA 3,{}(0) # load return adress".format(tPlace + offset)) # think about offset plus one inside of every function then subtract on for return address might be helpful
        
        self.addCode("LD 4,{}(0)  # load cmd line arg 1".format(tempArg1))
        
        self.addCode("LD 5,{}(0)  # load cmd line arg 2 or other known variable from dmem".format(arg2Offset + offset ))
        self.addCode("MUL 4,4,5   # multiply")
        if tempArg2 != None:
            self.addCode("ST 4,{}(0)  # store product in DMEM at same return address handed in".format(tPlace + offset)) # this should be stored in the function offset return not in a hard coded spot
        else:
            self.addCode("ST 4,1({})  # store product in DMEM at same return address handed in".format(offset))

        self.loadReg()
        #self.addCode("LDA 7,0(6) # branch back using r7") #still considering what the offset should be

    def genPrint(self, tempArg1, tempArg2, tempPlace):
        self.saveReg()
        self.addCode("LDC 2,{}(0)  # load cmd line arg 1".format(tempArg1))
        self.addCode("ST 2,{}(0)  # store cmd line arg 1".format(tempPlace + self._nextOffset))
        self.loadReg()
    
    
    
    def generate(self):
        
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