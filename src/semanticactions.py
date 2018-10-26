class AST_Node(object):
    pass
    
class Program_Node(AST_Node):
    def __init__(self, identifier, formals, definitions, body):
        self._identifier     = identifier
        self._formals        = formals
        self._definitions    = definitions
        self._body           = body

        
    def __str__(self):
        #return str(self.identifier())
        #return """Program {} Formals {} definitions {} body {}""".format(str(self.identifier()), str(self.formals()), str(self.definitions()), str(self.body()))
        idstr = "Program {}\n".format(str(self.identifier()))
        if self.formals() == None:
            formalsstr = ""
        else:
            formalsstr = "Formals {}\n".format(str(self.formals()))
        if self.definitions() == None:
            defsstr = ""
        else:
            defsstr = "Definitions {}\n".format(str(self.definitions()))
        bodystr = "\tBody\n{}\n".format(str(self.body()))
        return idstr + formalsstr + defsstr + bodystr
        
        
    def identifier(self):
        return self._identifier
        
    def formals(self):
        return self._formals
    
    def definitions(self):
        return self._definitions
    
    def body(self):
        return self._body
    
class Def_Node(AST_Node):
    def __init__(self, identifier, formals, type, body):
        self._identifier     = identifier
        self._formals        = formals
        self._type           = type
        self._body           = body
        
    def __str__(self):
        return """Function {} takes in {} returns a""".format(str(self.identifier()), str(self.formals()), str(self.type()))
        
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
        
    def __str__(self):
        return str(self.statementlist())
    
    def statementlist(self):
        return self._statementlist
        
class Integer_Node(AST_Node):
    def __init__(self, integer):
        self._integer = integer
        
    def __str__(self):
        if self.integer() == None:
            return "integer"
        else:
            return "{}".format(str(self.integer()))
        
    def integer(self):
        return self._integer
        
class Boolean_Node(AST_Node):
    def __init__(self, boolean):
        self._boolean = boolean
        
    def __str__(self):
        return str(self.boolean())
        
    def boolean(self, boolean):
        return self._boolean
        
class SimpleExpr_Node(AST_Node):
    def __init__(self, term, seprime):
        self._term = term
        self._seprime = seprime
        
    def __str__(self):
        if self.seprime() == None:
            return "{}".format(str(self.term()))
        else:
            return "{} {}".format(str(self.term()), str(self.seprime()))
        
    def term(self):
        return self._term
        
    def seprime(self):
        return self._seprime
        
class LessThan_Node(AST_Node):
    def __init__(self, simpleexpr):
        self._simpleexpr = simpleexpr
        
    def __str__(self):
        return "Less than {}".format(str(self.simpleexpr()))
        
    def simpleexpr(self):
        return self._simpleexpr
        
class EqualTo_Node(AST_Node):
    def __init__(self, simpleexpr):
        self._simpleexpr = simpleexpr
        
    def __str__(self):
        return "Equal to {}".format(self.simpleexpr())
        
    def simpleexpr(self):
        return self._simpleexpr
        
class Or_Node(AST_Node):
    def __init__(self, term):
        self._term = term
        
    def __str__(self):
        return "Or {}".format(str(self.term()))
        
    def term(self):
        return self._term
        
class Plus_Node(AST_Node):
    def __init__(self, term):
        self._term = term
        
    def __str__(self):
        return "Plus {}".format(str(self.term()))
        
    def term(self):
        return self._term
        
class Minus_Node(AST_Node):
    def __init__(self, term):
        self._term = term
        
    def __str__(self):
        return "Minus {}".format(str(self.term()))
        
    def term(self):
        return self._term    
        
class And_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def __str__(self):
        return "And {}".format(str(self.factor()))
        
    def factor(self):
        return self._factor
        
class Times_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def __str__(self):
        return "multiplied by {}".format(str(self.factor()))
        
    def factor(self):
        return self._factor
        
class Divide_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def __str__(self):
        return "Divided by {}".format(str(self.factor()))
        
    def factor(self):
        return self._factor
        
class If_Node(AST_Node):
    def __init__(self, expr1, expr2, expr3):
        self._expr1 = expr1
        self._expr2 = expr2
        self._expr3 = expr3
        
    def __str__(self):
        return """If {} then {} else {}""".format(str(self.expr1()), str(self.expr2()), str(self.expr3()))

    def expr1(self):
        return self._expr1

    def expr2(self):
        return self._expr2

    def expr3(self):
        return self._expr3        
        
class Not_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def __str__(self):
        return "Not {}".format(str(self.factor()))
        
    def factor(self):
        return self._factor
        
class Identifier_Node(AST_Node):
    def __init__(self, identifier):
        self._identifier = identifier

    def __str__(self):
        return str(self.identifier())

    def identifier(self):
        return self._identifier
        
class Literal_Node(AST_Node):
    def __init__(self, literal):
        self._literal = literal
        
    def __str__(self):
        return str(self.literal())
        
    def literal(self):
        return self._literal
        
class Negate_Node(AST_Node):
    def __init__(self, factor):
        self._factor = factor
        
    def __str__(self):
        return "Not {}".format(str(self.factor()))
        
    def factor(self):
        return self._factor
        
class Number_Node(AST_Node):
    def __init__(self, number):
        self._number = number
        
    def __str__(self):
        return str(self.number())
        
    def number(self):
        return self._number
        
class PrintStatement_Node(AST_Node):
    def __init__(self, expr):
        self._expr = expr
        
    def __str__(self):
        return "Print {}".format(str(self.expr()))
        
    def expr(self):
        return self._expr
        
class Formal_Node(AST_Node):
    def __init__(self, identifier, type):
        self._identifier = identifier
        self._type = type
        
    def __str__(self):
        return "{} is type {}".format(str(self.identifier()), str(self.type()))
        
    def identifier(self):
        return self._identifier
        
    def type(self):
        return self._type

class Formals_Node(AST_Node):
    def __init__(self, neformals):
        self._neformals = neformals #list of formals in program (list is empty if no formals,but node is still created)
        
    def __str__(self):
        if self.neformals() == None:
            return ""
        else:
            formalsstr = ""
            for formal in self.neformals():
                formalsstr = formalsstr + "{}, ".format(str(formal))
            return formalsstr
        #return "{}".format(str(self.neformals()))
        
    def neformals(self):
        return self._neformals   
  
class Definitions_Node(AST_Node):
    def __init__(self, deffs):
        self._deffs = deffs #list of definition nodes
        #self._definitions = definitions
        
    def __str__(self):
        defstr = ""
        for deff in self.deffs():
            defstr = defstr + "{}, ".format(str(deff))
        return defstr
        #return "{}".format(str(self.deffs()))
    
    def deffs(self):
        return self._deffs
        
    # def definitions(self):
        # return self._definitions
        
        
class StatementList_Node(AST_Node):
    def __init__(self, prints, returnstatement):
        self._prints = prints
        self._returnstatement = returnstatement
    
    def __str__(self):
        slstr = ""
        for statement in self.prints():
            slstr = slstr + "\t\tPrint {}\n".format(str(statement))
        return slstr + "\t\tReturn {}\n".format(str(self.returnstatement()))
        #return "{} {}".format(str(self.prints()), str(self.returnstatement()))
        
    def prints(self):
        return self._prints
        
    def returnstatement(self):
        return self._returnstatement
        
        
class Term_Node(AST_Node):
    def __init__(self, factor, termprime):
        self._factor = factor
        self._termprime = termprime
        
    def __str__(self):
        if self.termprime() == None:
            return "{}".format(str(self.factor()))
        else:
            return "{} {}".format(str(self.factor()), str(self.termprime()))
        
    def factor(self):
        return self._factor
        
    def termprime(self):
        return self._termprime
        
        
class Expr_Node(AST_Node):
    def __init__(self, sexpr, exprprime):
        self._sexpr = sexpr
        self._exprprime = exprprime
        
    def __str__(self):
        if self.exprprime() == None:
            return "{}".format(str(self.sexpr()))
        else:
            return "{} {}".format(str(self.sexpr()), str(self.exprprime()))
            
    def sexpr(self):
        return self._sexpr
        
    def exprprime(self):
        return self._exprprime
        
class Call_Node(AST_Node):
    def __init__(self, identifier, actuals):
        self._identifier = identifier
        self._actuals = actuals
        
    def __str__(self):
        return "{}({})".format(str(self.identifier()), str(self.actuals()))
        
    def identifier(self):
        return self._identifier
        
    def actuals(self):
        return self._actuals
        
class Actuals_Node(AST_Node):
    def __init__(self, actualList):
        self._actualList = actualList
        
    def __str__(self):
        actualstr = ""
        for actual in self.actualList():
            actualstr = actualstr = str(actual)
        return actualstr
    
    def actualList(self):
        return self._actualList