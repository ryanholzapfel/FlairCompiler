from semanticactions import *

class CodeGen(object):
    def __init__(self, programNode, symbolTable):
        self._programNode = programNode
        self._symbolTable = symbolTable
        self._programName = programNode.identifier().identifier()
        self._jumpString = ""
        self._currentLine = 0
        self._programString = ""
        self._labelData = {}
        self._jumpsToComplete = []
        self._availableIMEM = ["locked",0,0,0,0,1,1,"locked"] #locked = reserved (PC and const. 0), 0= not in use, 1= in use

    def toggleIMEM(self, regNum):
        if self._availableIMEM[regNum] == 0:
            self._availableIMEM[regNum] = 1
        elif self._availableIMEM[regNum] == 1:
            self._availableIMEM[regNum] = 0

    def regInUse(self, regNum):
        self._availableIMEM[regNum] = 1
    
    def regAvail(self, regNum):
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
        self.addCode("")

    def genMain(self):
        pass

    def saveReg(self):
        self.addCode("ST 0,1(5)   #save IMEM to DMEM")
        self.addCode("ST 1,2(5)   #save IMEM to DMEM")
        self.addCode("ST 2,3(5)   #save IMEM to DMEM")
        self.addCode("ST 3,4(5)   #save IMEM to DMEM")
        self.addCode("ST 4,5(5)   #save IMEM to DMEM")

    def loadReg(self):
        self.addCode("LD 0,1(5)   #load DMEM to IMEM")
        self.addCode("LD 1,2(5)   #load DMEM to IMEM")
        self.addCode("LD 2,3(5)   #load DMEM to IMEM")
        self.addCode("LD 3,4(5)   #load DMEM to IMEM")
        self.addCode("LD 4,5(5)   #load DMEM to IMEM")

    def initializeMain(self): #
        self.genPointers()
        self.storeReturn()
        #hardcoded save and set status pointer
        self.addCode("ST 5,7(6)")
        self.addCode("LDA 5,1(6)")
        self.addCode("ST 6,8(6)")
        self.addCode("LDA 6,9(6)")
        #end hardcode
        self.genJump() #make a jump for later
        self.addCode("LD#retrieve stored value")
        
    def storeReturn(self):
        self.addCode("LDA 1,6(7)  #load return address")
        self.addCode("ST 1,1(6)   #store return address")

    def genJump(self): #WIP
        self._jumpString = self._jumpString + str(self.currentLine()) + ": LDA 7, X(0)"
        self.incrementLine()

    def returnMain(self):
        #hardcode literal 1
        self.addCode("LDC 2,1(0)  #literal one")
        #end hardcode
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
        self.returnMain()
        return self._programString