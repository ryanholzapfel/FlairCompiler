from semanticactions import *

class SemanticAnalyzer(self, programNode):
	def __init__(self, programNode):
		self._programNode = programNode
		self._currentType = None
		self._errors = []
		self._typelist = {}
		
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
		
	def formals_list(self):
		for formal in self.programNode().formals():
			self._typelist[formal.identifier().identifier()] = formal.type()
		#return type_list
		
	def check_expr(node):
		if node.exprprime() == None:
			return check_se(node.sexpr())
		elif isinstance(node.exprprime(), LessThan_Node):
			if check_se(node.sexpr())=="I" and check_less(node.exprprime())=="I"
				return "B"
		else: #exprprime is an equal to node
			if check_se(node.sexpr())=="I" and check_equal(node.exprprime()):=="I"
				return "B"
			else:
				msg = "Int Error: Expected to resolve integer in equal to operation, got boolean"
				addError(msg)
				return "I"
			
	def check_se(node):
		if node.seprime() == None:
			return check_term(node.term())
		elif isinstance(node.seprime(), Or_Node):
			if check_term(node.term())=="B" and check_or(node.seprime())=="B"
				return "B"
			else:
				msg = "Bool Error: Expected to resolve boolean in OR operation, got Integer"
				addError(msg)
				return "I"
		elif isinstance(node.seprime(), Plus_Node):
			if check_term(node.term())=="I" and check_plus(node.seprime())=="I"
				return "B"
			else:
				msg = "Int Error: Expected to resolve addition operation to Integer, got Boolean"
				addError(msg)
				return "B"
		else: #seprime is a minus node
			if check_term(node.term())=="I" and check_minus(node.seprime())=="I"
				return "I"
			else:
				msg = "Int Error: Expected to resolve subtraction operation to Integer, got Boolean"
				addError(msg)
				return "B"
			
	def check_term(node):
		if node.termprime() == None:
			return check_factor(node.factor())
		elif isinstance(node.termprime(), Times_Node):
			if check_factor(node.factor())=="I" and check_times(node.termprime())=="I"
				return "I"
			else:
				msg = "Int Error: Expected to resolve multiplication operation to Integer, got Boolean"
				addError(msg)
				return "B"
		else: #termprime is a divide node
			if check_factor(node.factor())=="I" and check_divide(node.termprime()) == "I"
				return "I"
			else:
				msg = "Int Error: Expected to resolve division operation to Integer, got Boolean"
				addError(msg)
				return "B"
				
				
	def check_factor(self, node):
		if isinstance(node, Expr_Node):
			return check_expr(node)
		elif isinstance(node, If_Node):
			return check_if(node)
		elif isinstance(node, Not_Node):
			return check_not(node)
		elif isinstance(node, Literal_Node):# stores type int or boolean for later evaluations and returns true
		    if isinstance(node.literal(), Integer_Node):
				#setInteger()
				return "I"
			else:
				#setBool()
				return "B"
		elif isinstance(node, Identifier_Node):
			id = node.identifier()
			if isinstance(self._typelist[id], Integer_Node):
				return "I"
			else: # ID is assigned to boolean type
				return "B"		
		else: #factor is function call
			if isinstance(node.identifier(), Integer_Node):
				return "I"
			else: #function returns type boolean
				return "B"
				
				
				
				
				
				
				
				
				
				
				
				
				
				
	def table(self):
		formals_list()
		
			

			
	