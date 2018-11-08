from semanticactions import *

class SemanticAnalyzer(object):
    def __init__(self, programNode):
        self._programNode = programNode
        self._currentType = None
        self._errors = []
        self._typelist = {}
        self._currentID = ""
        
    def programNode(self):
        return self._programNode
        
    # def setBool(self):
        # self._currentType = "Boolean"
        
    # def setInt(self):
        # self._currentType = "Integer"
        
    def getType(self):
        return self._currentType

    def addError(self, msg):
        return self._errors.append(msg)
        
    def formals_dict(self, node): #node is the program node, creates a double dict for all formals in program
        # self._typeList = {} #empty out dict
        # programID = node.identifier().identifier()
        # self._typelist[programID] = {}
        # for formal in node.formals(): #build program formals set
        # 	self._typelist[programID][formal.identifier().identifier()] = formal.types()
        # defs = node.definitions()
        # for deff in defs: #for each def
        # 	defID = deff.identifier().identifier()
        # 	self._typelist[defID] = {}
        # 	for formal in deff.formals():
        # 		self._typelist[defID][formal.identifier().identifier()] = formal.types()
        programID = node.identifier().identifier()
        self._typelist[programID] = [[],[]]
        if not node.formals() == None:
            for formal in node.formals().neformals():
                self._typelist[programID][0].append(formal.identifier().identifier())
                self._typelist[programID][1].append(self.check_return(formal.types()))
        if not node.definitions() == None:   
            for deff in node.definitions().deffs():
                defID = deff.identifier().identifier()
                self._typelist[defID] = [[],[]]
                for formal in deff.formals().neformals():
                    self._typelist[defID][0].append(formal.identifier().identifier())
                    self._typelist[defID][1].append(self.check_return(formal.types()))
            

    def set_currentID(self,id):
        self._currentID = id
        
    def check_expr(self, node):
        print(node)
        if node.exprprime() == None:
            print("checked se only")
            return self.check_se(node.sexpr())
        elif isinstance(node.exprprime(), LessThan_Node):
            if self.check_se(node.sexpr())=="I" and self.check_less(node.exprprime())=="I":
                print("checked se and less")
                return "B"
        else: #exprprime is an equal to node
            if self.check_se(node.sexpr())=="I" and self.check_equal(node.exprprime())=="I":
                print("checked se and equal")
                return "B"
            else:
                msg = "Int Error: Expected to resolve integer in equal to operation, got boolean"
                self.addError(msg)
                return "I"
            
    def check_se(self, node):
        print(node.seprime(), "and", node.term)
        if node.seprime() == None:
            return self.check_term(node.term())
        elif isinstance(node.seprime(), Or_Node):
            if self.check_term(node.term())=="B" and self.check_or(node.seprime())=="B":
                return "B"
            else:
                msg = "Bool Error: Expected to resolve boolean in OR operation, got Integer"
                self.addError(msg)
                return "I"
        elif isinstance(node.seprime(), Plus_Node):
            if self.check_term(node.term())=="I" and self.check_plus(node.seprime())=="I":
                return "I"
            else:
                msg = "Int Error: Expected to resolve addition operation to Integer, got Boolean"
                self.addError(msg)
                return "B"
        else: #seprime is a minus node
            if self.check_term(node.term())=="I" and self.check_minus(node.seprime())=="I":
                return "I"
            else:
                msg = "Int Error: Expected to resolve subtraction operation to Integer, got Boolean"
                self.addError(msg)
                return "B"
            
    def check_term(self, node):
        if node.termprime() == None:
            return self.check_factor(node.factor())
        elif isinstance(node.termprime(), Times_Node):
            if self.check_factor(node.factor())=="I" and self.check_times(node.termprime())=="I":
                return "I"
            else:
                print(self.check_factor(node.factor()), self.check_times(node.termprime()))
                msg = "Int Error: Expected to resolve multiplication operation to Integer, got Boolean"
                self.addError(msg)
                return "B"
        elif isinstance(node.termprime(), And_Node):
            if self.check_factor(node.factor())=="B" and self.check_and(node.termprime())=="B":
                return "B"
            else:
                return "I"
        else: #termprime is a divide node
            if self.check_factor(node.factor())=="I" and self.check_divide(node.termprime()) == "I":
                return "I"
            else:
                msg = "Int Error: Expected to resolve division operation to Integer, got Boolean"
                self.addError(msg)
                return "B"
                
                
    def check_factor(self, node):
        if isinstance(node, Expr_Node):
            return self.check_expr(node)
        elif isinstance(node, If_Node):
            return self.check_if(node)
        elif isinstance(node, Not_Node):
            return self.check_not(node)
        elif isinstance(node, Literal_Node):# stores type int or boolean for later evaluations and returns true
            if isinstance(node.literal(), Integer_Node):
                return "I"
            elif isinstance(node.literal(), Boolean_Node):
                #setBool()
                return "B"
            else:
                print("couldn't resolve literal to either type", node.literal())
                return("I")
        elif isinstance(node, Identifier_Node):
            return self.check_id(node)
        elif isinstance(node, Call_Node):
            return self.check_call(node)

    def check_call(self, node):
        pass
                
                
                
    def check_equal(self, node):
        return self.check_se(node.simpleexpr())
        # if isinstance(node, Integer_Node):
        # 	return "I"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "B"
    def check_less(self, node):
        return self.check_se(node.simpleexpr())
        # if isinstance(node, Integer_Node):
        # 	return "I"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "B"
    def check_plus(self, node):
        return self.check_term(node.term())
        # if isinstance(node, Integer_Node):
        # 	return "I"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "B"
    def check_minus(self, node):
        return self.check_term(node.term())
        # if isinstance(node, Integer_Node):
        # 	return "I"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "B"
    def check_or(self, node):
        return self.check_term(node.term())
        # if isinstance(node, Boolean_Node):
        # 	return "B"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "I"
    def check_times(self, node):
        return self.check_factor(node.factor())
        # if isinstance(node, Integer_Node):
        # 	return "I"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "B"
    def check_divide(self, node):
        return self.check_factor(node.factor())
        # if isinstance(node, Integer_Node):
        # 	return "I"
        # elif isinstance(node, Identifier_Node):
        # 	return check_id(node)
        # else:
        # 	return "B"
    def check_if(self, node):
        tf = self.check_expr(node.expr1())
        rt = self.check_expr(node.expr2())
        rf = self.check_expr(node.expr3())
        if tf == "B":
            if rt == rf:
                return rt
            else:
                msg = "Mismatch return types on If-Then-Else"
                addError(msg)
                return "B" #doesn't matter what this returns...
        else:
            msg = "If statement does not evaluate to boolean"
            addError(msg)
            return "I"

    def check_not(self, node):
        return self.check_factor(node.factor())

    def check_negate(self, node):
        return self.check_factor(node.factor())

    def check_and(self, node):
        return self.check_factor(node.factor())
                
    def check_id(self, node):
        idstr = node.identifier() 
        #if node is id, look up id in formals type list and check if integer or boolean
        idindex = self._typelist[self._currentID][0].index(idstr)
        formalType = self._typelist[self._currentID][1][idindex]
        if formalType == "I": #isinstance(formalType, Integer_Node):
            return "I"
        elif formalType == "B": #isinstance(formalType, Boolean_Node): # ID is assigned to boolean type
            return "B"
        else:
            print("couldn't resolve id to type", idstr)
            return "I"
                
    def check_return(self, node):
        #print(node)
        if isinstance(node, Integer_Node):
            return "I"
        elif isinstance(node, Boolean_Node):
            return "B"
        else:
            print("couldn't resolve return type")
            return "I"
        

    def check_def(self, node):	#node is def node	
        expr_type = self.check_expr(node.body().statementlist().returnstatement())
        return_type = self.check_return(node.types())
        if expr_type == return_type:
            #print(expr_type)
            return expr_type
        else:
            msg = "def {} expected {} return type got {}".format(self._currentID, expr_type, return_type)
            self.addError(msg)

    def check_definitions(self, node): #node is program node
        for deff in node.definitions().deffs():
            self.set_currentID(deff.identifier().identifier())
            valid = self.check_def(deff)

    def check_program(self, node):
        self.set_currentID(node.identifier().identifier())
        expr_type = self.check_expr(node.body().statementlist().returnstatement())
        return expr_type


                
                
                
                
                
                
    def table(self):
        self.formals_dict(self.programNode())
        #print(self._typelist)
        self.check_definitions(self.programNode())
        self.check_program(self.programNode())
        print(self._errors)
        programFunctions = []
        #functionList = []
        for function in self.programNode().definitions().deffs():
            functionList = []
            functionList.append(str(function.identifier()))
            functionList.append(str(function.formals()))
            functionList.append(str(function.types()))
            programFunctions.append(str(functionList))
        print(programFunctions)
        
            

            
    