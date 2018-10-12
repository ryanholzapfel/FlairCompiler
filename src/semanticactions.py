class AST_Node(object):
    pass
    
class Program_Node(AST_Node):
    def __init__(self, identifier, formals, definitions, body):
        self._identifier     = identifier
        self._formals        = formals
        self._definitions    = definitions
        self._body           = body
        
    def identifier(self):
        return self._identifier
        
    def formals(self):
        return self._formals
    
    def definitions(self):
        return self._definitions
    
    def body(self):
        return self._body
    
class Def_Node(AST_Node):
    def __init__(self, identifier, formals, definitions, body):
        self._identifier     = identifier
        self._formals        = formals
        self._type           = type
        self._body           = body
        
    def identifier(self):
        return self._identifier
        
    def formals(self):
        return self._formals
        
    def type(self):
        return self._type
        
    def body(self):
        return self._body
    
class Body_Node(AST_Node):
    def __init__(self, statementlist):
        self._statementlist  = statementlist
    
    def statementlist(self):
        return self._statementlist
        
class Integer_Node(AST_Node):
    def __init__(self, integer):
        self._integer = integer
        
    def interger(self, integer):
        return self._integer
        
class Boolean_Node(AST_Node):
    def __init__(self, boolean):
        self._boolean = boolean
        
    def boolean(self, boolean):
        return self._boolean
        
class SimpleExpr_Node(AST_Node):
    def __init__(self, term, seprime):
        self._term = term
        self._seprime = seprime
        
    def term(self):
        return self._term
        
    def seprime(self):
        return self._seprime
        
class LessThan_Node(AST_Node):
    def __init__(self, simpleexpr):
        self._simpleexpr = simpleexpr
        
    def simpleexpr(self):
        return self._simpleexpr
        
class EqualTo_Node(AST_Node):
    def __init__(self, simpleexpr):
        self._simpleexpr = simpleexpr
        
    def simpleexpr(self):
        return self._simpleexpr
        
class Or_Node(AST_Node):
    def __init__(self, term):
        self._term = term
        
    def term(self):
        return self._term
        
class Plus_Node(AST_Node):
    def __init__(self, term):
        self._term = term
        
    def term(self):
        return self._term
        
class Minus_Node(AST_Node):
    def __init__(self, term):
        self._term = term
        
    def term(self):
        return self._term    
        
class And_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def factor(self):
        return self._factor
        
class Times_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def factor(self):
        return self._factor
        
class Divide_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def factor(self):
        return self._factor
        
class If_Node(AST_Node):
    def __init__(self, expr1, expr2, expr3):
        self._expr1 = expr1
        self._expr2 = expr2
        self._expr3 = expr3

    def expr1(self):
        return self._expr1

    def expr2(self):
        return self._expr2

    def expr3(self):
        return self._expr3        
        
class Not_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def factor(self):
        return self._factor
        
class Identifier_Node(AST_Node):
    def __init__(self, identifier):
        self._identifier = identifier
        
    def identifier(self):
        return self._identifier
        
class Literal_Node(AST_Node):
    def __init__(self, literal):
        self._literal = literal
        
    def literal(self):
        return self._literal
        
class Negate_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def factor(self):
        return self._factor
        
class Number_Node(AST_Node):
    def __init__(self, number):
        self._number = number
        
    def number(self):
        return self._number
        
class PrintStatement_Node(AST_Node):
    def __init__(self, expr):
        self._expr = expr
        
    def expr(self):
        return self._expr
        
class Formal_Node(AST_Node):
    def __init__(self, identifier, type):
        self._identifier = identifier
        self._type = type
        
    def identifier(self):
        return self._identifier
        
    def type(self):
        return self._type
        
class Definitions_Node(AST_Node):
    def __init__(self, deff, definitions):
        self._deff = deff
        self._definitions = definitions
    
    def deff(self):
        return self._deff
        
    def definitions(self):
        return self._definitions
        
        