from semanticactions import *

# This class should take in a tree node program and return a list of lists that has quadruples.
# The list will be inorder tree traversal of the program node.
# The quadruples in the list will be in format [<operator>,<Arg1>,<Arg2>,<tempLocation>]

class GenExpression(Enum):
    genMult     = 1
    genDiv      = 2
    genAdd      = 3
    genSubt     = 4
    genLess     = 5
    genEqual    = 6
    genOr       = 7
    genIf       = 8
    genAnd      = 9
    genNot      = 10
    genNeg      = 11
    genPrint    = 12
    genReturn   = 13
    genBool     = 14

class threeACGen(object):
    def __init__(self, programNode, symbolTable):
        self._programNode = programNode
        self._symbolTable = symbolTable #list of lists containing all functions used in program 
        self._program3AC = []

    def lessThan(self):
        self._exprPrime.place = makeNewTemp()
        self._exprPrime.code =  [simpleExpr1.code]
                                [simpleExpr2.code]

def idInc(id):
    num = int(id[1:])
    return "t" + str(num+1)

def new3AC(id,op,a1,a2):
    pass

def program3AC(returnExpr): #returnExpr is the return expression from the program node
    id = "t1"
    acList = []
    #need a backlog/temp list for the case where both sides of an operator are expressions



def walkExpr(expr):
    if not expr.exprprime() == None:
        pass
    walkSimpleExpr(expr.sexpr())

def walkSimpleExpr(simpleexpr):
    if not simpleexpr.seprime() == None:
        pass
    walkTerm(simpleexpr.term())

def walkTerm(term):
    if not term.termprime() == None:
        pass
    walkFactor(term.factor())

def walkFactor(factor):
    if isinstance(factor,Literal_Node):
        return factor.literal()
    elif isinstance(factor, Identifier_Node):
        return factor.identifier()
    elif isinstance(factor, If_Node):
        pass
    elif isinstance(factor, Call_Node):
        pass
    else: #make sure I didn't forget any...
        walkExpr(factor)
                                emitCode(exprPrime.place,":=",simpleExpr1.place "<", simpleExpr2.place)

