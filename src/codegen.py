from semanticactions import *

class CodeGen(object):
    def __init__(self, programNode, symbolTable):
        self._programNode = programNode
        self._symbolTable = symbolTable
        self._threeAddressList = []
        self._currentNode = programNode
        self._programStr = ""

    def programNode(self):
        return self._programNode

    def symbolTable(self):
        return self._symbolTable

    def threeAddressList(self):
        return self._threeAddressList

    def currentNode(self):
        return self._currentNode

    def programStr(self):
        return self._programStr

    def addInstructions(self, instructions):
        self._programStr = self._programStr + instructions

    def threeAddressWriter(self, first, op, second):
        #create a new 3AC
        self._threeAddressList.append([first, op, second])

    def threeAddressEdit(self, inst, first, op, second):
        #can only be used if a 3AC has already been created / written
        if not first == None:
            self._threeAddressList[inst][0] = first
        if not op == None:
            self._threeAddressList[inst][1] = op
        if not second == None:
            self._threeAddressList[inst][2] = second

    def walkReturn(self):
        #walk left side of program return
        factor = self.programNode().body().statementlist().returnstatement().sexpr().term().factor()
        if isinstance(factor, Literal_Node):
            firstLiteral = factor.literal()
            if isinstance(firstLiteral, Boolean_Node):
                if firstLiteral.boolean() == "true":
                    firstLiteral = 1
                else:
                    firstLiteral = 0
            # else:
            #     firstLiteral = firstLiteral.integer()
        # termprime = self.programNode.().body().statementlist().returnstatement().simpleexpr().term().termprime()
        # if not termprime == None:
        #     #there is a multiply, divide, or AND operation
        #     op = termprime
        self.threeAddressWriter(firstLiteral, None, None)
        #print(self._threeAddressList)

    def tmWriter(self, codenum):
        #currently, this is only going to load a literal constant
        talist = self.threeAddressList()
        if not talist[codenum][0] == None:
            self.addInstructions("LDC 2,{}(0)\n".format(talist[codenum][0]))
        if not talist[codenum][1] == None: #if not none, there is an operation to perform
            #add the second literal 
            self.addInstructions("LDC 3,{}(0)\n".format(talist[codenum][2]))
            #perform the operation
            #big if isinstance checking what operation needs to be added


    def generate(self):
        self.walkReturn()
        for code in range(0,len(self.threeAddressList())):
            self.tmWriter(code)
        self.addInstructions("OUT 2,0,0\nHALT 0,0,0")
        self.addLineNumbers()
        #print(self.programStr())
        return self.programStr()
            

    def addLineNumbers(self):
        pstr = self.programStr()
        #pstr = "0:  " + pstr
        plist = pstr.split("\n")
        instnum = 0
        pstr = ""
        for inst in plist:
            pstr = pstr + str(instnum) + ":  " + inst + "\n"
            #inst = str(instnum) + ":  " + inst
            instnum += 1
        #print(pstr)
        self._programStr = pstr