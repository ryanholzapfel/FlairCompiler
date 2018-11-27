from semanticactions import *

class CodeGen(object):
    def __init__(self, programNode, symbolTable):
        self._programNode = programNode
        self._symbolTable = symbolTable #list of lists containing all functions used in program 
        self._programName = programNode.identifier().identifier() #sting of the name of program being compiled
        self._jumpString = ['*--------- BackPatched Jumps\n'] # a string of all backpached jumps
        self._currentLine = 0 #current tm line number
        self._programString = "" # sting of all tm lines in the program
        self._labelData = {} # dict of labels used in jumps
        self._jumpsToComplete = []
        self._availableIMEM = ["locked",0,0,0,0,1,1,"locked"] #locked = reserved (PC and const. 0), 0= not in use, 1= in use
        self._currentLabel = 1

    def toggleIMEM(self, regNum):
        if self._availableIMEM[regNum] == 0:
            self._availableIMEM[regNum] = 1
        elif self._availableIMEM[regNum] == 1:
            self._availableIMEM[regNum] = 0

    def currentLabel(self):
        tempLabel = "label" + str(self._currentLabel)
        self._currentLabel += 1
        return tempLabel  

    def regInUse(self, regNum):# used to toggle available imem register as in use
        self._availableIMEM[regNum] = 1
    
    def regAvail(self, regNum):# used to toggle in use imem register as available
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
        self.addCode("") #use getRegister()and increment through args from the symbol table for that specific function
        progArgs= self._symbolTable[self._programName]
        for arg in progArgs: # how i get the arg here is wrong i for got where the args are passed in possibly in the tree???
            tempReg = getRegister()
            self.addCode("LDC {},{}(0)  #load arg".format(tempReg, arg))#need to save command line arg here 
            self.addCode('ST {},{},(10) #save arg to dmem'.format(tempReg, arg.index())) # to find arg in dmem use the index in symboyl table of arg desired plus an offset of 10
            #IMPORTANT: we should set up an offset in case there are more than 3 args passed in. which is highly probable
            #IMPORTANT: if we decide to store function variables in dmem we need to count keep track of all args and previous variables saved in dmem 
            #  or we risk overwriting important dmem registers
            #IMPORTANT: we still need to handle 0 arg cases we can do this by looking at the bottom of the program node to see what value is returned, 
            # then load that as our arg, this will probably only be useful in print one style cases we only do this if symbol table has 0 args

        treeValue = 1 # not sure how to get the actuall tree value here
        if len(self._symbolTable[self._programName]) == 0:
            self.addCode('LDC 2,{}(0) #load zero arg case'.format(treeValue))

            # would look like --> self.addCode("LDC {},{}({})  #load arg".format(getRegister(), arg, offset)) where offset is determinde either by the number of args in symbol table or set at a constant 10
            #might have to keep track of how mnay times getRegister is called 

            # i dont toggle the registers here because i save the args to dmem. if we choose to optimize we can toggle registers especially if there 
            # are 3 args or less so that we dont have to reload them later in the secuence. it would likely help by reducing stack size

    def genTMProgram(self):
        self.initializeMain()
        

    def saveReg(self): # typically used to store imem before a function call to save current state of main prog
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

    def initializeMain(self): #
        self.genPointers()
        self.storeReturn()
        #hardcoded save and set status pointer
        #self.addCode("ST 5,7(6)")
        #self.addCode("LDA 5,1(6)")
        #self.addCode("ST 6,8(6)")
        #self.addCode("LDA 6,9(6)")
        #end hardcode
        
        thisLabel = self.currentLabel()
        self._jumpsToComplete.append((self.currentLine() ,thisLabel, 'uncondtional' ))
        self._labelData[thisLabel] = self.currentLine() + 1
        self.incrementLine()
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
        genProgramArgs()
        #not hardcoded WIP
        #self.addCode("LDC 2,{}(0)  #literal one".format(commandArg))#need to save command line arg here
        #
        
        self.addCode("OUT 2,0,0   #return result of main")
        self.addCode("HALT 0,0,0  #stop execution; end of program")


    def nextOperation(self):
        pass

    def genMult(self, a,b,c): #r2 is possibly not zero
        self.saveReg()
        self.addCode("LDA 3,{}(0) #".format(a))
        self.addCode("LD 4,{}(0)  #".format(b))
        self.addCode("LD 5,{}(0)  #".format(c))
        self.addCode("MUL 4,4,5   #multiply")
        self.addCode("ST 4,0(3)   #store product in DMEM")
        self.loadReg()
        
    def generate(self):
        self.genPointers()
        self.initializeMain()
        

        return self._programString