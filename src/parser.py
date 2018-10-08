#parser.py
#table driven parser for flair

from scanner import Scanner

from flair_tokens import Token, TokenType

from error   import ParseError, SemanticError

from enum import Enum

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
    stack.pop()

def push_rule(lst, stack):
    for element in reversed(lst):
        stack.append(element)


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
                                                 TokenType.END],
    (NonTerminal.DEF, TokenType.FUNCTION): [   TokenType.FUNCTION,
                                                   TokenType.IDENTIFIER,
                                                   TokenType.LEFTPARENT,
                                                   NonTerminal.FORMALS,
                                                   TokenType.RIGHTPARENT,
                                                   TokenType.COLON,
                                                   NonTerminal.TYPE,
                                                   NonTerminal.BODY,
                                                   TokenType.SEMICOLON],
    (NonTerminal.DEFINITIONS, TokenType.BEGIN): [],
    (NonTerminal.DEFINITIONS, TokenType.EOF): [],
    (NonTerminal.DEFINITIONS, TokenType.FUNCTION): [   NonTerminal.DEF,
                                                           NonTerminal.DEFINITIONS],
    (NonTerminal.EXPR, TokenType.BOOLEAN): [   NonTerminal.SIMPLEEXPR,
                                                   NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.IDENTIFIER): [   NonTerminal.SIMPLEEXPR,
                                                      NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.IF): [   NonTerminal.SIMPLEEXPR,
                                              NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.LEFTPARENT): [   NonTerminal.SIMPLEEXPR,
                                                      NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.NOT): [   NonTerminal.SIMPLEEXPR,
                                               NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.NUMBER): [   NonTerminal.SIMPLEEXPR,
                                                  NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.SUBTRACT): [   NonTerminal.SIMPLEEXPR,
                                                    NonTerminal.EXPRPRIME],
    (NonTerminal.EXPRPRIME, TokenType.ELSE): [],
    (NonTerminal.EXPRPRIME, TokenType.END): [],
    (NonTerminal.EXPRPRIME, TokenType.EOF): [],
    (NonTerminal.EXPRPRIME, TokenType.EQUAL): [   TokenType.EQUAL,
                                                      NonTerminal.SIMPLEEXPR],
    (NonTerminal.EXPRPRIME, TokenType.LESS): [   TokenType.LESS,
                                                     NonTerminal.SIMPLEEXPR],
    (NonTerminal.EXPRPRIME, TokenType.RIGHTPARENT): [],
    (NonTerminal.EXPRPRIME, TokenType.THEN): [],
    (NonTerminal.FACTOR, TokenType.BOOLEAN): [NonTerminal.LITERAL],
    (NonTerminal.FACTOR, TokenType.IDENTIFIER): [   TokenType.IDENTIFIER,
                                                        NonTerminal.FACTORREST],
    (NonTerminal.FACTOR, TokenType.IF): [   TokenType.IF,
                                                NonTerminal.EXPR,
                                                TokenType.THEN,
                                                NonTerminal.EXPR,
                                                TokenType.ELSE,
                                                NonTerminal.EXPR],
    (NonTerminal.FACTOR, TokenType.LEFTPARENT): [   TokenType.LEFTPARENT,
                                                        NonTerminal.EXPR,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.NOT): [   TokenType.NOT,
                                                 NonTerminal.FACTOR],
    (NonTerminal.FACTOR, TokenType.NUMBER): [NonTerminal.LITERAL],
    (NonTerminal.FACTOR, TokenType.SUBTRACT): [   TokenType.SUBTRACT,
                                                      NonTerminal.FACTOR],
    (NonTerminal.FACTORREST, TokenType.ADD): [],
    (NonTerminal.FACTORREST, TokenType.AND): [],
    (NonTerminal.FACTORREST, TokenType.DIVIDE): [],
    (NonTerminal.FACTORREST, TokenType.ELSE): [],
    (NonTerminal.FACTORREST, TokenType.END): [],
    (NonTerminal.FACTORREST, TokenType.EOF): [],
    (NonTerminal.FACTORREST, TokenType.EQUAL): [],
    (NonTerminal.FACTORREST, TokenType.LEFTPARENT): [   TokenType.LEFTPARENT,
                                                            NonTerminal.ACTUALS,
                                                            TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.LESS): [],
    (NonTerminal.FACTORREST, TokenType.MULTIPLY): [],
    (NonTerminal.FACTORREST, TokenType.OR): [],
    (NonTerminal.FACTORREST, TokenType.RIGHTPARENT): [],
    (NonTerminal.FACTORREST, TokenType.SUBTRACT): [],
    (NonTerminal.FACTORREST, TokenType.THEN): [],
    (NonTerminal.FORMAL, TokenType.IDENTIFIER): [   TokenType.IDENTIFIER,
                                                        TokenType.COLON,
                                                        NonTerminal.TYPE],
    (NonTerminal.FORMALS, TokenType.EOF): [],
    (NonTerminal.FORMALS, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYFORMALS],
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
                                                                NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.EOF): [],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.IF): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.LEFTPARENT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.NOT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.NUMBER): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.RIGHTPARENT): [   ],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.SUBTRACT): [   NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYFORMALS, TokenType.IDENTIFIER): [   NonTerminal.FORMAL,
                                                                 NonTerminal.NONEMPTYFORMALSREST],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.EOF): [],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.RIGHTPARENT): [   ],
    (NonTerminal.PRINTSTATEMENT, TokenType.PRINT): [   TokenType.PRINT,
                                                           TokenType.LEFTPARENT,
                                                           NonTerminal.EXPR,
                                                           TokenType.RIGHTPARENT,
                                                           TokenType.SEMICOLON],
    (NonTerminal.PROGRAM, TokenType.program): [   TokenType.program,
                                                      TokenType.IDENTIFIER,
                                                      TokenType.LEFTPARENT,
                                                      NonTerminal.FORMALS,
                                                      TokenType.RIGHTPARENT,
                                                      TokenType.SEMICOLON,
                                                      NonTerminal.DEFINITIONS,
                                                      NonTerminal.BODY,
                                                      TokenType.PERIOD],
    (NonTerminal.SEPRIME, TokenType.ADD): [   TokenType.ADD,
                                                  NonTerminal.TERM],
    (NonTerminal.SEPRIME, TokenType.ELSE): [],
    (NonTerminal.SEPRIME, TokenType.END): [],
    (NonTerminal.SEPRIME, TokenType.EOF): [],
    (NonTerminal.SEPRIME, TokenType.EQUAL): [],
    (NonTerminal.SEPRIME, TokenType.LESS): [],
    (NonTerminal.SEPRIME, TokenType.OR): [   TokenType.OR,
                                                 NonTerminal.TERM],
    (NonTerminal.SEPRIME, TokenType.RIGHTPARENT): [],
    (NonTerminal.SEPRIME, TokenType.SUBTRACT): [   TokenType.SUBTRACT,
                                                       NonTerminal.TERM],
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
                                                           NonTerminal.EXPR],
    (NonTerminal.STATEMENTREST, TokenType.COMMA): [   TokenType.COMMA,
                                                          NonTerminal.STATEMENTLIST],
    (NonTerminal.STATEMENTREST, TokenType.END): [],
    (NonTerminal.STATEMENTREST, TokenType.EOF): [],
    (NonTerminal.STATEMENTREST, TokenType.PRINT): [   NonTerminal.STATEMENTLIST],
    (NonTerminal.TERM, TokenType.BOOLEAN): [   NonTerminal.FACTOR,
                                                   NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.IDENTIFIER): [   NonTerminal.FACTOR,
                                                      NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.IF): [   NonTerminal.FACTOR,
                                              NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.LEFTPARENT): [   NonTerminal.FACTOR,
                                                      NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.NOT): [   NonTerminal.FACTOR,
                                               NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.NUMBER): [   NonTerminal.FACTOR,
                                                  NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.SUBTRACT): [   NonTerminal.FACTOR,
                                                    NonTerminal.TERMPRIME],
    (NonTerminal.TERMPRIME, TokenType.ADD): [],
    (NonTerminal.TERMPRIME, TokenType.AND): [   TokenType.AND,
                                                    NonTerminal.FACTOR],
    (NonTerminal.TERMPRIME, TokenType.DIVIDE): [   TokenType.DIVIDE,
                                                       NonTerminal.FACTOR],
    (NonTerminal.TERMPRIME, TokenType.ELSE): [],
    (NonTerminal.TERMPRIME, TokenType.END): [],
    (NonTerminal.TERMPRIME, TokenType.EOF): [],
    (NonTerminal.TERMPRIME, TokenType.EQUAL): [],
    (NonTerminal.TERMPRIME, TokenType.LESS): [],
    (NonTerminal.TERMPRIME, TokenType.MULTIPLY): [   TokenType.MULTIPLY,
                                                         NonTerminal.FACTOR],
    (NonTerminal.TERMPRIME, TokenType.OR): [],
    (NonTerminal.TERMPRIME, TokenType.RIGHTPARENT): [],
    (NonTerminal.TERMPRIME, TokenType.SUBTRACT): [],
    (NonTerminal.TERMPRIME, TokenType.THEN): [],
    (NonTerminal.TYPE, TokenType.BOOLEAN): [TokenType.BOOLEAN],
    (NonTerminal.TYPE, TokenType.NUMBER): [TokenType.NUMBER]}








#Parser 
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        
    def parse(self):
        parseStack = []
        semanticStack = []
        push_rule([NonTerminal.PROGRAM, TokenType.EOF], parseStack)
        while parseStack:
            print("full stack", parseStack)
            grammarRule = top(parseStack)
            print("top of stack",grammarRule)
            if isinstance( grammarRule, TokenType):
                t = self.scanner.next_token()
                print("next token",t.token_type)
                if grammarRule == t.token_type:
                    pop(parseStack)
                else:
                    msg ='token mismatch: {} and {}'
                    raise ParseError(msg.format(grammarRule,t))
            elif isinstance( grammarRule, NonTerminal):
                t = self.scanner.peek()
                print("expand on", grammarRule, t.token_type)
                rule = parse_table.get( (grammarRule, t.token_type))
                if rule != None:
                    pop(parseStack)
                    push_rule(rule, parseStack)
                else:
                    msg = 'cannot expand {} on {}'
                    raise ParseError(msg.format(grammarRule,t))
            else:
                msg = 'invalid item on stack: {}'
                raise ParseError(msg.format(grammarRule))
                    
        if not t.is_eof():
            msg = 'unexpected token at end: {}'
            raise ParseError(msg.format(t))
                        
        return True
