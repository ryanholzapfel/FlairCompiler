from semanticactions import *

class GenExpression(Enum):
    genMult = 1
    genDiv = 2
    genAdd = 3
    genSubt = 4
    genLess = 5
    genEqual = 6
    genOr = 7
    genIf = 8
    genAnd = 9
    genNot = 10
    genNeg = 11
    genPrint = 12
    genReturn = 13
    genBool = 14

class threeACGen(object):
    def __init__(self, programNode, symbolTable):
        self._programNode = programNode
        self._symbolTable = symbolTable #list of lists containing all functions used in program 
        self._program3AC = []

    def lessThan(self):
        self._exprPrime.place = makeNewTemp()
        self._exprPrime.code =  [simpleExpr1.code]
                                [simpleExpr2.code]
<<<<<<< HEAD
                                if isinstance()
                                emitCode(exprPrime.place,":=",simpleExpr1.place "<", simpleExpr2.place)

    
=======
                                emitCode(exprPrime.place,":=",simpleExpr1.place "<", simpleExpr2.place)

>>>>>>> 2babaa8514002b32c27ecc3611aef764a5b97d27
