#ast_ops.py
#holds AST node creation operations for parser

#import AST Tree Node classes
from semanticactions import *

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