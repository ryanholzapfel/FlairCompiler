#parser.py
#table driven parser for flair

from scanner import Scanner

from flair_tokens import Token, TokenType

from error   import ParseError, SemanticError

from enum import Enum

from semanticactions import *

# non-terminals

class NonTerminal(Enum):
    PROGRAM    = 0
    DEFINITIONS      = 1
    DEF = 2
    FORMALS  = 3
    NONEMPTYFORMALS        = 4
    FORMAL      = 5
    NONEMPTYFORMALSREST    = 6               
    BODY                    = 7
    STATEMENTLIST          = 8       
    TYPE                    = 9
    EXPR                    = 10
    EXPRPRIME              = 11  
    SIMPLEEXPR             = 12    
    SEPRIME                = 13
    TERM                    = 14
    TERMPRIME              = 15  
    FACTOR                  = 16
    FACTORREST             = 17      
    ACTUALS                 = 18
    NONEMPTYACTUALS         = 19      
    NONEMPTYACTUALSREST    = 20        
    LITERAL                 = 21
    PRINTSTATEMENT         = 22 
    STATEMENTREST        = 23    
    
#Stack Operations
def top(stack):
    return stack[-1]

def pop(stack):
    return stack.pop()

def push_rule(lst, stack):
    for element in reversed(lst):
        stack.append(element)

def push(item, stack):
    stack.append(item)

        
        
        
        
        
class Ast_Type(Enum): 
    make_program =1 
    make_def =2 
    make_body =3 
    make_integer =4 
    make_boolean =5 
    make_simpleexpr =6 
    make_lessthan =7 
    make_equalto =8 
    make_or =9 
    make_plus =10 
    make_minus =11 
    make_and =12 
    make_times =13 
    make_divide =14 
    make_if =15 
    make_not =16 
    make_identifier =17 
    make_literal =18 
    make_negate =19 
    make_number =20 
    make_printstatement =21  
    make_formal = 22
    make_definitions = 23
    make_formals = 24
    make_statementlist = 25
    make_term = 26
    make_expr = 27
    make_call = 28
    make_actuals = 29
    
#Semantic Action node creation functions
def make_definitions_node(ast_stack):
    deffs = []
    while isinstance(top(ast_stack), Def_Node): #as long as the top of the stack is a def, add it to the definitions node
      deffs.append(pop(ast_stack))
    node = Definitions_Node(deffs)
    push(node, ast_stack)

def make_formal_node(ast_stack):
    type = pop(ast_stack)
    identifier = pop(ast_stack)
    node = Formal_Node(identifier,type)
    push(node, ast_stack)

def make_formals_node(ast_stack):
    neformals = []
    while isinstance(top(ast_stack), Formal_Node): #as long as the top of the stack is a formal, add it to the formals node
      neformals.append(pop(ast_stack))
    # if neformals == []:
        # node = Formals_Node(None)
    # else:
        # node = Formals_Node(neformals)
    node = Formals_Node(neformals)
    push(node, ast_stack)
    
    
def make_program_node(ast_stack):
    body = pop(ast_stack)
    if isinstance(top(ast_stack), Definitions_Node):
        definitions = pop(ast_stack)
    else:
        definitions = None
    if isinstance(top(ast_stack), Formals_Node):
        formals = pop(ast_stack)
    else:
        formals = None
    identifier = pop(ast_stack)
    node = Program_Node(identifier,formals,definitions,body)
    push(node, ast_stack)

def make_def_node(ast_stack):
    body = pop(ast_stack)
    type = pop(ast_stack)
    formals = pop(ast_stack)
    identifier = pop(ast_stack)
    node = Def_Node(identifier,formals,type,body)
    push(node, ast_stack)
    
def make_body_node(ast_stack):
    statementlist = pop(ast_stack)
    node = Body_Node(statementlist)
    push(node, ast_stack)
    
def make_integer_node(ast_stack):
    integer = pop(ast_stack)
    node = Integer_Node(integer)
    push(node, ast_stack)
    
def make_boolean_node(ast_stack):
    boolean = pop(ast_stack)
    node = Boolean_Node(boolean)
    push(node, ast_stack)

def make_simpleexpr_node(ast_stack):
    if isinstance(top(ast_stack), Or_Node) or isinstance(top(ast_stack), Minus_Node) or isinstance(top(ast_stack), Plus_Node):
        seprime = pop(ast_stack)
    else:
        seprime = None
    term = pop(ast_stack)
    node = SimpleExpr_Node(term, seprime)
    push(node, ast_stack)
    
def make_lessthan_node(ast_stack):
    simpleexpr = pop(ast_stack)
    node = LessThan_Node(simpleexpr)
    push(node, ast_stack)
    
def make_equalto_node(ast_stack):
    simpleexpr = pop(ast_stack)
    node = EqualTo_Node(simpleexpr)
    push(node, ast_stack)
    
def make_or_node(ast_stack):
    term = pop(ast_stack)
    node = Or_Node(term)
    push(node, ast_stack)
    
def make_plus_node(ast_stack):
    term = pop(ast_stack)
    node = Plus_Node(term)
    push(node, ast_stack)
    
def make_minus_node(ast_stack):
    term = pop(ast_stack)
    node = Minus_Node(term)
    push(node, ast_stack)
    
def make_and_node(ast_stack):
    factor = pop(ast_stack)
    node = And_Node(factor)
    push(node, ast_stack)
    
def make_times_node(ast_stack):
    factor = pop(ast_stack)
    node = Times_Node(factor)
    push(node, ast_stack)
    
def make_divide_node(ast_stack):
    factor = pop(ast_stack)
    node = Divide_Node(factor)
    push(node, ast_stack)
    
def make_if_node(ast_stack):
    expr3 = pop(ast_stack)
    expr2 = pop(ast_stack)
    expr1 = pop(ast_stack)
    node = If_Node(expr1,expr2,expr3)
    push(node, ast_stack)
    
def make_not_node(ast_stack):
    factor = pop(ast_stack)
    node = Not_Node(factor)
    push(node, ast_stack)
    
def make_identifier_node(ast_stack):
    identifier = pop(ast_stack)
    node = Identifier_Node(identifier)
    push(node, ast_stack)
    
def make_literal_node(ast_stack):
    literal = pop(ast_stack)
    node = Literal_Node(literal)
    push(node, ast_stack)
    
def make_negate_node(ast_stack):
    factor = pop(ast_stack)
    node = Negate_Node(factor)
    push(node, ast_stack)
    
def make_number_node(ast_stack):
    number = pop(ast_stack)
    node = Number_Node(number)
    push(node, ast_stack)
    
def make_printstatement_node(ast_stack):
    expr = pop(ast_stack)
    node = PrintStatement_Node(expr)
    push(node, ast_stack)
    
    
def make_statementlist_node(ast_stack):
    returnstatement = pop(ast_stack)
    prints = []
    while isinstance(top(ast_stack), PrintStatement_Node):
      prints.append(pop(ast_stack))
    node = StatementList_Node(prints,returnstatement)
    push(node, ast_stack)
    
def make_term_node(ast_stack):
    if isinstance(top(ast_stack), Times_Node) or isinstance(top(ast_stack), Divide_Node):
        termprime = pop(ast_stack)
    else:
        termprime = None
    factor = pop(ast_stack)
    node = Term_Node(factor, termprime)
    push(node, ast_stack)
    

def make_expr_node(ast_stack):
    if isinstance(top(ast_stack), LessThan_Node) or isinstance(top(ast_stack), EqualTo_Node):
        exprprime = pop(ast_stack)
    else:
        exprprime = None
    sexpr = pop(ast_stack)
    node = Expr_Node(sexpr, exprprime)
    push(node, ast_stack)
    
def make_call_node(ast_stack):
    # actuals = []
    # while isinstance(top(ast_stack), Expr_Node):
        # actuals.append(pop(ast_stack))
    if isinstance(top(ast_stack), Actuals_Node):
        actuals = pop(ast_stack)
    else:
        actuals = None
    identifier = pop(ast_stack)
    node = Call_Node(identifier, actuals)
    push(node, ast_stack)


def make_actuals_node(ast_stack):
    actuals = []
    while isinstance(top(ast_stack), Expr_Node):
        actuals.append(pop(ast_stack))
    node = Actuals_Node(actuals)
    push(node, ast_stack)
    
    
action_table = {
    Ast_Type.make_program : make_program_node, 
    Ast_Type.make_def : make_def_node, 
    Ast_Type.make_body : make_body_node, 
    Ast_Type.make_integer : make_integer_node, 
    Ast_Type.make_boolean : make_boolean_node, 
    Ast_Type.make_simpleexpr : make_simpleexpr_node, 
    Ast_Type.make_lessthan : make_lessthan_node, 
    Ast_Type.make_equalto : make_equalto_node, 
    Ast_Type.make_or : make_or_node, 
    Ast_Type.make_plus : make_plus_node, 
    Ast_Type.make_minus : make_minus_node, 
    Ast_Type.make_and : make_and_node, 
    Ast_Type.make_times : make_times_node, 
    Ast_Type.make_divide : make_divide_node, 
    Ast_Type.make_if : make_if_node, 
    Ast_Type.make_not : make_not_node, 
    Ast_Type.make_identifier : make_identifier_node, 
    Ast_Type.make_literal : make_literal_node, 
    Ast_Type.make_negate : make_negate_node, 
    Ast_Type.make_number : make_number_node, 
    Ast_Type.make_printstatement : make_printstatement_node,
    Ast_Type.make_formal : make_formal_node,
    Ast_Type.make_definitions : make_definitions_node,
    Ast_Type.make_formals : make_formals_node,
    Ast_Type.make_statementlist : make_statementlist_node,
    Ast_Type.make_term : make_term_node,
    Ast_Type.make_expr : make_expr_node,
    Ast_Type.make_call : make_call_node,
    Ast_Type.make_actuals : make_actuals_node}
   
#parse table
parse_table = {   (NonTerminal.ACTUALS, TokenType.BOOLEAN): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.EOF): [],
    (NonTerminal.ACTUALS, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.IF): [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.LEFTPARENT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.NOT): [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.NUMBER): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.RIGHTPARENT): [],
    (NonTerminal.ACTUALS, TokenType.SUBTRACT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.BODY, TokenType.BEGIN): [   TokenType.BEGIN,
                                                 NonTerminal.STATEMENTLIST,
                                                 TokenType.END,
                                                 Ast_Type.make_body],
    (NonTerminal.DEF, TokenType.FUNCTION): [   TokenType.FUNCTION,
                                                   TokenType.IDENTIFIER,
                                                   Ast_Type.make_identifier,
                                                   TokenType.LEFTPARENT,
                                                   NonTerminal.FORMALS,
                                                   TokenType.RIGHTPARENT,
                                                   TokenType.COLON,
                                                   NonTerminal.TYPE,
                                                   NonTerminal.BODY,
                                                   TokenType.SEMICOLON,
                                                   Ast_Type.make_def],
    (NonTerminal.DEFINITIONS, TokenType.BEGIN): [],
    (NonTerminal.DEFINITIONS, TokenType.EOF): [],
    (NonTerminal.DEFINITIONS, TokenType.FUNCTION): [   NonTerminal.DEF,
                                                           NonTerminal.DEFINITIONS],
    (NonTerminal.EXPR, TokenType.BOOLEAN): [   NonTerminal.SIMPLEEXPR,
                                                   Ast_Type.make_simpleexpr,
                                                   NonTerminal.EXPRPRIME,
                                                   Ast_Type.make_expr],
    (NonTerminal.EXPR, TokenType.COMMA): [],
    (NonTerminal.EXPR, TokenType.IDENTIFIER): [   NonTerminal.SIMPLEEXPR,
                                                      Ast_Type.make_simpleexpr,
                                                      NonTerminal.EXPRPRIME,
                                                      Ast_Type.make_expr],
    (NonTerminal.EXPR, TokenType.IF): [   NonTerminal.SIMPLEEXPR,
                                              Ast_Type.make_simpleexpr,
                                              NonTerminal.EXPRPRIME,
                                              Ast_Type.make_expr],
    (NonTerminal.EXPR, TokenType.LEFTPARENT): [   NonTerminal.SIMPLEEXPR,
                                                      Ast_Type.make_simpleexpr,
                                                      NonTerminal.EXPRPRIME,
                                                      Ast_Type.make_expr],
    (NonTerminal.EXPR, TokenType.NOT): [   NonTerminal.SIMPLEEXPR,
                                               Ast_Type.make_simpleexpr,
                                               NonTerminal.EXPRPRIME,
                                               Ast_Type.make_expr],
    (NonTerminal.EXPR, TokenType.NUMBER): [   NonTerminal.SIMPLEEXPR,
                                                  Ast_Type.make_simpleexpr,
                                                  NonTerminal.EXPRPRIME,
                                                  Ast_Type.make_expr],
    (NonTerminal.EXPR, TokenType.SUBTRACT): [   NonTerminal.SIMPLEEXPR,
                                                    Ast_Type.make_simpleexpr,
                                                    NonTerminal.EXPRPRIME,
                                                    Ast_Type.make_expr],
    (NonTerminal.EXPRPRIME, TokenType.AND): [   TokenType.AND,
                                                    NonTerminal.FACTOR],
    (NonTerminal.EXPRPRIME, TokenType.COMMA): [],
    (NonTerminal.EXPRPRIME, TokenType.DIVIDE): [   TokenType.DIVIDE,
                                                       NonTerminal.FACTOR],
    (NonTerminal.EXPRPRIME, TokenType.ELSE): [],
    (NonTerminal.EXPRPRIME, TokenType.END): [],
    (NonTerminal.EXPRPRIME, TokenType.EOF): [],
    (NonTerminal.EXPRPRIME, TokenType.EQUAL): [   TokenType.EQUAL,
                                                      NonTerminal.SIMPLEEXPR,
                                                      Ast_Type.make_equalto],
    (NonTerminal.EXPRPRIME, TokenType.LESS): [   TokenType.LESS,
                                                     NonTerminal.SIMPLEEXPR,
                                                     Ast_Type.make_lessthan],
    (NonTerminal.EXPRPRIME, TokenType.MULTIPLY): [   TokenType.MULTIPLY,
                                                         NonTerminal.FACTOR],
    (NonTerminal.EXPRPRIME, TokenType.RIGHTPARENT): [],
    (NonTerminal.EXPRPRIME, TokenType.THEN): [],
    (NonTerminal.FACTOR, TokenType.BOOLEAN): [   NonTerminal.LITERAL,
                                                     Ast_Type.make_literal],
    (NonTerminal.FACTOR, TokenType.IDENTIFIER): [   TokenType.IDENTIFIER,
                                                        NonTerminal.FACTORREST],
    (NonTerminal.FACTOR, TokenType.IF): [   TokenType.IF,
                                                NonTerminal.EXPR,
                                                TokenType.THEN,
                                                NonTerminal.EXPR,
                                                TokenType.ELSE,
                                                NonTerminal.EXPR,
                                                Ast_Type.make_if],
    (NonTerminal.FACTOR, TokenType.LEFTPARENT): [   TokenType.LEFTPARENT,
                                                        NonTerminal.EXPR,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.NOT): [   TokenType.NOT,
                                                 NonTerminal.FACTOR,
                                                 Ast_Type.make_not],
    (NonTerminal.FACTOR, TokenType.NUMBER): [   NonTerminal.LITERAL,
                                                    Ast_Type.make_literal],
    (NonTerminal.FACTOR, TokenType.SUBTRACT): [   TokenType.SUBTRACT,
                                                      NonTerminal.FACTOR,
                                                      Ast_Type.make_negate],
    (NonTerminal.FACTORREST, TokenType.ADD): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.AND): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.COMMA): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.DIVIDE): [   Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.ELSE): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.END): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.EOF): [],
    (NonTerminal.FACTORREST, TokenType.EQUAL): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.LEFTPARENT): [   TokenType.LEFTPARENT,
                                                            NonTerminal.ACTUALS,
                                                            TokenType.RIGHTPARENT,
                                                            Ast_Type.make_call],
    (NonTerminal.FACTORREST, TokenType.LESS): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.MULTIPLY): [   Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.OR): [Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.RIGHTPARENT): [   Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.SUBTRACT): [   Ast_Type.make_identifier],
    (NonTerminal.FACTORREST, TokenType.THEN): [Ast_Type.make_identifier],
    (NonTerminal.FORMAL, TokenType.IDENTIFIER): [   TokenType.IDENTIFIER,
                                                        Ast_Type.make_identifier,
                                                        TokenType.COLON,
                                                        NonTerminal.TYPE,
                                                        Ast_Type.make_formal],
    (NonTerminal.FORMALS, TokenType.EOF): [],
    (NonTerminal.FORMALS, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYFORMALS,
                                                         Ast_Type.make_formals],
    (NonTerminal.FORMALS, TokenType.RIGHTPARENT): [],
    (NonTerminal.LITERAL, TokenType.BOOLEAN): [TokenType.BOOLEAN],
    (NonTerminal.LITERAL, TokenType.NUMBER): [TokenType.NUMBER],
    (NonTerminal.NONEMPTYACTUALS, TokenType.BOOLEAN): [   NonTerminal.EXPR,
                                                              NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.EOF): [],
    (NonTerminal.NONEMPTYACTUALS, TokenType.IDENTIFIER): [   NonTerminal.EXPR,
                                                                 NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.IF): [   NonTerminal.EXPR,
                                                         NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.LEFTPARENT): [   NonTerminal.EXPR,
                                                                 NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.NOT): [   NonTerminal.EXPR,
                                                          NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.NUMBER): [   NonTerminal.EXPR,
                                                             NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.RIGHTPARENT): [],
    (NonTerminal.NONEMPTYACTUALS, TokenType.SUBTRACT): [   NonTerminal.EXPR,
                                                               NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.BOOLEAN): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.COMMA): [   TokenType.COMMA,
                                                                NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.EOF): [],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.IF): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.LEFTPARENT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.NOT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.NUMBER): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.RIGHTPARENT): [   Ast_Type.make_actuals],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.SUBTRACT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYFORMALS, TokenType.IDENTIFIER): [   NonTerminal.FORMAL,
                                                                 NonTerminal.NONEMPTYFORMALSREST],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.COMMA): [   TokenType.COMMA,
                                                                NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.EOF): [],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.RIGHTPARENT): [   ],
    (NonTerminal.PRINTSTATEMENT, TokenType.PRINT): [   TokenType.PRINT,
                                                           TokenType.LEFTPARENT,
                                                           NonTerminal.EXPR,
                                                           TokenType.RIGHTPARENT,
                                                           TokenType.SEMICOLON,
                                                           Ast_Type.make_printstatement],
    (NonTerminal.PROGRAM, TokenType.program): [   TokenType.program,
                                                      TokenType.IDENTIFIER,
                                                      Ast_Type.make_identifier,
                                                      TokenType.LEFTPARENT,
                                                      NonTerminal.FORMALS,
                                                      TokenType.RIGHTPARENT,
                                                      TokenType.SEMICOLON,
                                                      NonTerminal.DEFINITIONS,
                                                      Ast_Type.make_definitions,
                                                      NonTerminal.BODY,
                                                      TokenType.PERIOD,
                                                      Ast_Type.make_program],
    (NonTerminal.SEPRIME, TokenType.ADD): [   TokenType.ADD,
                                                  NonTerminal.TERM,
                                                  Ast_Type.make_plus],
    (NonTerminal.SEPRIME, TokenType.COMMA): [],
    (NonTerminal.SEPRIME, TokenType.ELSE): [],
    (NonTerminal.SEPRIME, TokenType.END): [],
    (NonTerminal.SEPRIME, TokenType.EOF): [],
    (NonTerminal.SEPRIME, TokenType.EQUAL): [],
    (NonTerminal.SEPRIME, TokenType.LESS): [],
    (NonTerminal.SEPRIME, TokenType.OR): [   TokenType.OR,
                                                 NonTerminal.TERM,
                                                 Ast_Type.make_or],
    (NonTerminal.SEPRIME, TokenType.RIGHTPARENT): [],
    (NonTerminal.SEPRIME, TokenType.SUBTRACT): [   TokenType.SUBTRACT,
                                                       NonTerminal.TERM,
                                                       Ast_Type.make_minus],
    (NonTerminal.SEPRIME, TokenType.THEN): [],
    (NonTerminal.SIMPLEEXPR, TokenType.BOOLEAN): [   NonTerminal.TERM,
                                                         NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.IDENTIFIER): [   NonTerminal.TERM,
                                                            NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.IF): [   NonTerminal.TERM,
                                                    NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.LEFTPARENT): [   NonTerminal.TERM,
                                                            NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.NOT): [   NonTerminal.TERM,
                                                     NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.NUMBER): [   NonTerminal.TERM,
                                                        NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.SUBTRACT): [   NonTerminal.TERM,
                                                          NonTerminal.SEPRIME],
    (NonTerminal.STATEMENTLIST, TokenType.PRINT): [   NonTerminal.PRINTSTATEMENT,
                                                          NonTerminal.STATEMENTREST],
    (NonTerminal.STATEMENTLIST, TokenType.RETURN): [   TokenType.RETURN,
                                                           NonTerminal.EXPR,
                                                           Ast_Type.make_statementlist],
    (NonTerminal.STATEMENTREST, TokenType.COMMA): [   TokenType.COMMA,
                                                          NonTerminal.STATEMENTLIST],
    (NonTerminal.STATEMENTREST, TokenType.END): [],
    (NonTerminal.STATEMENTREST, TokenType.EOF): [],
    (NonTerminal.STATEMENTREST, TokenType.PRINT): [   NonTerminal.STATEMENTLIST],
    (NonTerminal.STATEMENTREST, TokenType.RETURN): [   NonTerminal.STATEMENTLIST],
    (NonTerminal.TERM, TokenType.BOOLEAN): [   NonTerminal.FACTOR,
                                                   NonTerminal.TERMPRIME,
                                                   Ast_Type.make_term],
    (NonTerminal.TERM, TokenType.IDENTIFIER): [   NonTerminal.FACTOR,
                                                      NonTerminal.TERMPRIME,
                                                      Ast_Type.make_term],
    (NonTerminal.TERM, TokenType.IF): [   NonTerminal.FACTOR,
                                              NonTerminal.TERMPRIME,
                                              Ast_Type.make_term],
    (NonTerminal.TERM, TokenType.LEFTPARENT): [   NonTerminal.FACTOR,
                                                      NonTerminal.TERMPRIME,
                                                      Ast_Type.make_term],
    (NonTerminal.TERM, TokenType.NOT): [   NonTerminal.FACTOR,
                                               NonTerminal.TERMPRIME,
                                               Ast_Type.make_term],
    (NonTerminal.TERM, TokenType.NUMBER): [   NonTerminal.FACTOR,
                                                  NonTerminal.TERMPRIME,
                                                  Ast_Type.make_term],
    (NonTerminal.TERM, TokenType.SUBTRACT): [   NonTerminal.FACTOR,
                                                    NonTerminal.TERMPRIME,
                                                    Ast_Type.make_term],
    (NonTerminal.TERMPRIME, TokenType.ADD): [],
    (NonTerminal.TERMPRIME, TokenType.AND): [   TokenType.AND,
                                                    NonTerminal.FACTOR,
                                                    Ast_Type.make_and],
    (NonTerminal.TERMPRIME, TokenType.COMMA): [],
    (NonTerminal.TERMPRIME, TokenType.DIVIDE): [   TokenType.DIVIDE,
                                                       NonTerminal.FACTOR,
                                                       Ast_Type.make_divide],
    (NonTerminal.TERMPRIME, TokenType.ELSE): [],
    (NonTerminal.TERMPRIME, TokenType.END): [],
    (NonTerminal.TERMPRIME, TokenType.EOF): [],
    (NonTerminal.TERMPRIME, TokenType.EQUAL): [],
    (NonTerminal.TERMPRIME, TokenType.LESS): [],
    (NonTerminal.TERMPRIME, TokenType.MULTIPLY): [   TokenType.MULTIPLY,
                                                         NonTerminal.FACTOR,
                                                         Ast_Type.make_times],
    (NonTerminal.TERMPRIME, TokenType.OR): [],
    (NonTerminal.TERMPRIME, TokenType.RIGHTPARENT): [],
    (NonTerminal.TERMPRIME, TokenType.SUBTRACT): [],
    (NonTerminal.TERMPRIME, TokenType.THEN): [],
    (NonTerminal.TYPE, TokenType.BOOLEAN): [   TokenType.BOOLEAN,
                                                   Ast_Type.make_boolean],
    (NonTerminal.TYPE, TokenType.NUMBER): [   TokenType.NUMBER,
                                                  Ast_Type.make_integer]}







































#Parser 
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        
    def parse(self):
        tokenCount = 0
        parseStack = []
        semanticStack = []
        push_rule([NonTerminal.PROGRAM, TokenType.EOF], parseStack)
        while parseStack:
            #print("full stack", parseStack)
            grammarRule = top(parseStack)
            #print("top of stack",grammarRule)
            if isinstance( grammarRule, TokenType):
                t = self.scanner.next()
                #print(tokenCount)
                tokenCount += 1
                #print("next token",t.token_type)
                if grammarRule == t.token_type:
                    if t.is_number() or t.is_boolean() or t.is_word():
                        push(t.value(), semanticStack)
                    pop(parseStack)
                else:
                    msg ='token mismatch: expected {} got {}'
                    raise ParseError(msg.format(grammarRule,t))
            elif isinstance( grammarRule, NonTerminal):
                t = self.scanner.peek()
                #print("expand on", grammarRule, t.token_type)
                rule = parse_table.get( (grammarRule, t.token_type))
                if rule != None:
                    pop(parseStack)
                    push_rule(rule, parseStack)
                else:
                    msg = 'cannot expand {} on {}'
                    raise ParseError(msg.format(grammarRule,t))
            elif isinstance(grammarRule, Ast_Type):
                #print(grammarRule, "/", semanticStack)#, semanticStack)
                actionNode = action_table.get(grammarRule) #lookup function to create node
                actionNode(semanticStack) #call function to create node
                pop(parseStack) #pop semantic action from parse stack
            else:
                msg = 'invalid item on stack: {}'
                raise ParseError(msg.format(grammarRule))
                    
        if not t.is_eof():
            msg = 'unexpected token at end: {}'
            raise ParseError(msg.format(t))
                        
        #print(semanticStack)
        #print(semanticStack[0])
        #for item in semanticStack:
            #print(item)
        return semanticStack[0]
