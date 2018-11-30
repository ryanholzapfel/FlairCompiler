from semanticactions import *
from enum import Enum

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

# class threeACGen(object):
#     def __init__(self, programNode, symbolTable):
#         self._programNode = programNode
#         self._symbolTable = symbolTable #list of lists containing all functions used in program 
#         self._program3AC = []

#     def lessThan(self):
#         self._exprPrime.place = makeNewTemp()
#         self._exprPrime.code =  [simpleExpr1.code]
#                                 [simpleExpr2.code]

class ThreeACGen():
    def __init__(self,programNode):
        self._programNode = programNode
        self._acList = []



    def idInc(self,id):
        num = int(id[1:])
        return "t" + str(num+1)

    def new3AC(self,op,a1,a2,id):
        self._acList.append([op,a1,a2,id])

    def program3AC(self,returnExpr): #returnExpr is the return expression from the program node
        id = "t1"
        #acList = [] #[[op, arg1, arg2, id]]
        #need a backlog/temp list for the case where both sides of an operator are expressions
        #acList.append(["t1", None, walkExpr(returnExpr), None])
        self.walkExpr(id,returnExpr)
        print(self._acList)



    def walkExpr(self,id,expr):
        if not expr.exprprime() == None:
            #find which operation node
            #find value on right side of operator
            if isinstance(expr.exprprime(), EqualTo_Node):
                op = GenExpression.genEqual
            else:
                op = GenExpression.genLess
            rid = self.idInc(id)
            lid = self.idInc(rid)
            self.new3AC(op,rid,lid,id)
            #walk down right side, then left
            self.walkSimpleExpr(rid,expr.exprprime().simpleexpr())
            self.walkSimpleExpr(lid,expr.sexpr())
        else:
            #walk down the tree
            self.walkSimpleExpr(id, expr.sexpr())
        #return walkSimpleExpr(expr.sexpr())


    def walkSimpleExpr(self,id,simpleexpr):
        if not simpleexpr.seprime() == None:
            if isinstance(simpleexpr.seprime(), Or_Node):
                op = GenExpression.genOr
            elif isinstance(simpleexpr.seprime(), Plus_Node):
                op = GenExpression.genAdd
            elif isinstance(simpleexpr.seprime(), Minus_Node):
                op = GenExpression.genSubt
            rid = self.idInc(id)
            lid = self.idInc(rid)
            self.new3AC(op,rid,lid, id)
            #walk right then left
            self.walkTerm(rid, simpleexpr.seprime().term())
            self.walkTerm(lid, simpleexpr.term())
            
        else:
            self.walkTerm(id,simpleexpr.term())

    def walkTerm(self,id,term):
        if not term.termprime() == None:
            if isinstance(term.termprime(), Times_Node):
                op = GenExpression.genMult
            elif isinstance(term.termprime(), Divide_Node):
                op = GenExpression.genDiv
            else: #isinstance and node
                op = GenExpression.genAnd
            rid = self.idInc(id)
            lid = self.idInc(rid)
            self.new3AC(op,rid,lid, id)
            #walk right then left
            rr = self.walkFactor(rid, term.termprime().factor())
            ll = self.walkFactor(lid, term.factor())
            for n in [rr, ll]:
                if isinstance(n, Negate_Node) or isinstance(n, Call_Node) or isinstance(n, Expr_Node):
                    pass
                else:
                    if n == ll:
                        nid = lid
                    else:
                        nid = rid
                    self.new3AC(None,None,n,nid)

        else:
            n = self.walkFactor(id,term.factor())
            if isinstance(n, Negate_Node) or isinstance(n, Call_Node) or isinstance(n, Expr_Node):
                pass
            else:
                self.new3AC(None,None,n,id)

    def walkFactor(self,id,factor):
        if isinstance(factor,Literal_Node):
            return factor.literal()
        elif isinstance(factor, Identifier_Node):
            return factor.identifier()
        elif isinstance(factor, If_Node):
            pass
        elif isinstance(factor, Call_Node):
            pass
        else: #make sure I didn't forget any...
            return self.walkExpr(factor)
                                #emitCode(exprPrime.place,":=",simpleExpr1.place "<", simpleExpr2.place)

