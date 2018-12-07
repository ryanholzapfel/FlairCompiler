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
    genCall     = 15



#object that stores 3AC, has functions that generate it from the program node
class ThreeACGen():
    def __init__(self,programNode):
        self._programNode = programNode #AST object
        self._acList = [] #list of 3AC fourples
        self._lastID = "t-1" #start at t-1 to increment to t0 when the first generate is called


    #increment the 3AC ID (eg. t0 -> t1)
    def idInc(self,id):
        num = int(id[1:])
        nextID = "t" + str(num+1)
        self._lastID = nextID
        return nextID

    def nextID(self,id):
        num = int(id[1:])
        nextID = "t" + str(num+1)
        return nextID

    #helper function, adds a 3AC fourple to the list
    def new3AC(self,op,a1,a2,id):
        self._acList.append([op,a1,a2,id])


    #call this to generate 3AC for whole function
    def program3AC(self):
        #generate 3AC for main return
        self.genExpr3AC(self._programNode.body().statementlist().returnstatement(), "t-1")
        #generate 3AC for each function definition
        for deff in self._programNode.definitions().deffs():
            #nextID = self.idInc(self._lastID)
            for code in self._acList:
                if deff.identifier().identifier() == code[2]:
                    code[1] = self.nextID(self._lastID)
            self.genExpr3AC(deff.body().statementlist().returnstatement(), self._lastID)
        return self._acList

    #generate 3AC from a return expression node
    def genExpr3AC(self,returnExpr, prevID): #returnExpr is the return statement from any function or main return
        id = self.idInc(prevID)
        #id = "t0"
        #acList = [] #[[op, arg1, arg2, id]]
        #need a backlog/temp list for the case where both sides of an operator are expressions
        #acList.append(["t1", None, walkExpr(returnExpr), None])
        self.walkExpr(id,returnExpr)
        #print(self._acList)
        #return self._acList


    #walk down the tree, see what operations there are
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
            if isinstance(n, Negate_Node):
                pass
            elif isinstance(n, Expr_Node):
                self.walkExpr(id, n)
            elif isinstance(n, Call_Node):
                #self.new3AC(GenExpression.genCall,self._acList[-1][-1],n.identifier(),id)
                self.new3AC(GenExpression.genCall,None,n.identifier(),id)
                id = self.idInc(id)
                actuals = n.actuals().actualList()
                for actual in actuals:
                    self.walkExpr(id,actual)
            else:
                self.new3AC(None,None,n,id)

    def walkFactor(self,id,factor):
        if isinstance(factor,Literal_Node):
            return factor.literal()
        elif isinstance(factor, Identifier_Node):
            return factor.identifier()
        elif isinstance(factor, If_Node):
            return factor
        elif isinstance(factor, Call_Node):
            return factor
        else: #make sure I didn't forget any...
            return self.walkExpr(factor)
