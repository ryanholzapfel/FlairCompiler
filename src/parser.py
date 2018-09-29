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
    
#Stack Operations
def top(stack):
    return stack[-1]

def pop(stack):
    stack.pop()

def push_rule(lst, stack):
    for element in reversed(lst):
        stack.append(element)


#parse table
parse_table = {   (NonTerminal.ACTUALS, TokenType.EOF): [],
    (NonTerminal.BODY, TokenType.BEGIN): [   TokenType.BEGIN,
                                                   NonTerminal.STATEMENTLIST,
                                                   TokenType.END],
    (NonTerminal.BODY, TokenType.END): [   TokenType.BEGIN,
                                                 NonTerminal.STATEMENTLIST,
                                                 TokenType.END],
    (NonTerminal.DEF, TokenType.COLON): [   TokenType.FUNCTION,
                                                  TokenType.IDENTIFIER,
                                                  TokenType.LEFTPARENT,
                                                  NonTerminal.FORMALS,
                                                  TokenType.RIGHTPARENT,
                                                  TokenType.COLON,
                                                  NonTerminal.TYPE,
                                                  NonTerminal.BODY,
                                                  TokenType.SEMICOLON],
    (NonTerminal.DEF, TokenType.FUNCTION): [   TokenType.FUNCTION,
                                                     TokenType.IDENTIFIER,
                                                     TokenType.LEFTPARENT,
                                                     NonTerminal.FORMALS,
                                                     TokenType.RIGHTPARENT,
                                                     TokenType.COLON,
                                                     NonTerminal.TYPE,
                                                     NonTerminal.BODY,
                                                     TokenType.SEMICOLON],
    (NonTerminal.DEF, TokenType.IDENTIFIER): [   TokenType.FUNCTION,
                                                       TokenType.IDENTIFIER,
                                                       TokenType.LEFTPARENT,
                                                       NonTerminal.FORMALS,
                                                       TokenType.RIGHTPARENT,
                                                       TokenType.COLON,
                                                       NonTerminal.TYPE,
                                                       NonTerminal.BODY,
                                                       TokenType.SEMICOLON],
    (NonTerminal.DEF, TokenType.LEFTPARENT): [   TokenType.FUNCTION,
                                                       TokenType.IDENTIFIER,
                                                       TokenType.LEFTPARENT,
                                                       NonTerminal.FORMALS,
                                                       TokenType.RIGHTPARENT,
                                                       TokenType.COLON,
                                                       NonTerminal.TYPE,
                                                       NonTerminal.BODY,
                                                       TokenType.SEMICOLON],
    (NonTerminal.DEF, TokenType.RIGHTPARENT): [   TokenType.FUNCTION,
                                                        TokenType.IDENTIFIER,
                                                        TokenType.LEFTPARENT,
                                                        NonTerminal.FORMALS,
                                                        TokenType.RIGHTPARENT,
                                                        TokenType.COLON,
                                                        NonTerminal.TYPE,
                                                        NonTerminal.BODY,
                                                        TokenType.SEMICOLON],
    (NonTerminal.DEF, TokenType.SEMICOLON): [   TokenType.FUNCTION,
                                                      TokenType.IDENTIFIER,
                                                      TokenType.LEFTPARENT,
                                                      NonTerminal.FORMALS,
                                                      TokenType.RIGHTPARENT,
                                                      TokenType.COLON,
                                                      NonTerminal.TYPE,
                                                      NonTerminal.BODY,
                                                      TokenType.SEMICOLON],
    (NonTerminal.DEFINITIONS, TokenType.BEGIN): [   NonTerminal.DEF,
                                                          NonTerminal.DEFINITIONS],
    (NonTerminal.DEFINITIONS, TokenType.EOF): [],
    (NonTerminal.EXPR, TokenType.ELSE): [   NonTerminal.SIMPLEEXPR,
                                                  NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.END): [   NonTerminal.SIMPLEEXPR,
                                                 NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.EOF): [   NonTerminal.SIMPLEEXPR,
                                                 NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.RIGHTPARENT): [   NonTerminal.SIMPLEEXPR,
                                                         NonTerminal.EXPRPRIME],
    (NonTerminal.EXPR, TokenType.THEN): [   NonTerminal.SIMPLEEXPR,
                                                  NonTerminal.EXPRPRIME],
    (NonTerminal.EXPRPRIME, TokenType.EOF): [],
    (NonTerminal.EXPRPRIME, TokenType.EQUAL): [   TokenType.EQUAL,
                                                        NonTerminal.SIMPLEEXPR],
    (NonTerminal.EXPRPRIME, TokenType.LESS): [   TokenType.LESS,
                                                       NonTerminal.SIMPLEEXPR],
    (NonTerminal.FACTOR, TokenType.DIVIDE): [   TokenType.LEFTPARENT,
                                                      NonTerminal.EXPR,
                                                      TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.ELSE): [   TokenType.IF,
                                                    NonTerminal.EXPR,
                                                    TokenType.THEN,
                                                    NonTerminal.EXPR,
                                                    TokenType.ELSE,
                                                    NonTerminal.EXPR],
    (NonTerminal.FACTOR, TokenType.EOF): [   TokenType.IDENTIFIER,
                                                   NonTerminal.FACTORREST],
    (NonTerminal.FACTOR, TokenType.EQUAL): [   TokenType.LEFTPARENT,
                                                     NonTerminal.EXPR,
                                                     TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.IDENTIFIER): [   TokenType.IDENTIFIER,
                                                          NonTerminal.FACTORREST],
    (NonTerminal.FACTOR, TokenType.IF): [   TokenType.IF,
                                                  NonTerminal.EXPR,
                                                  TokenType.THEN,
                                                  NonTerminal.EXPR,
                                                  TokenType.ELSE,
                                                  NonTerminal.EXPR],
    (NonTerminal.FACTOR, TokenType.LESS): [   TokenType.LEFTPARENT,
                                                    NonTerminal.EXPR,
                                                    TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.SUBTRACT): [   TokenType.SUBTRACT,
                                                     NonTerminal.FACTOR],
    (NonTerminal.FACTOR, TokenType.MULTIPLY): [   TokenType.LEFTPARENT,
                                                        NonTerminal.EXPR,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.NOT): [   TokenType.NOT,
                                                   NonTerminal.FACTOR],
    (NonTerminal.FACTOR, TokenType.ADD): [   TokenType.LEFTPARENT,
                                                    NonTerminal.EXPR,
                                                    TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.RIGHTPARENT): [   TokenType.LEFTPARENT,
                                                           NonTerminal.EXPR,
                                                           TokenType.RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.THEN): [   TokenType.IF,
                                                    NonTerminal.EXPR,
                                                    TokenType.THEN,
                                                    NonTerminal.EXPR,
                                                    TokenType.ELSE,
                                                    NonTerminal.EXPR],
    (NonTerminal.FACTORREST, TokenType.AND): [   TokenType.LEFTPARENT,
                                                       NonTerminal.ACTUALS,
                                                       TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.DIVIDE): [   TokenType.LEFTPARENT,
                                                          NonTerminal.ACTUALS,
                                                          TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.ELSE): [   TokenType.LEFTPARENT,
                                                        NonTerminal.ACTUALS,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.END): [   TokenType.LEFTPARENT,
                                                       NonTerminal.ACTUALS,
                                                       TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.EOF): [],
    (NonTerminal.FACTORREST, TokenType.EQUAL): [   TokenType.LEFTPARENT,
                                                         NonTerminal.ACTUALS,
                                                         TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.LEFTPARENT): [   TokenType.LEFTPARENT,
                                                              NonTerminal.ACTUALS,
                                                              TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.LESS): [   TokenType.LEFTPARENT,
                                                        NonTerminal.ACTUALS,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.SUBTRACT): [   TokenType.LEFTPARENT,
                                                         NonTerminal.ACTUALS,
                                                         TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.MULTIPLY): [   TokenType.LEFTPARENT,
                                                            NonTerminal.ACTUALS,
                                                            TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.OR): [   TokenType.LEFTPARENT,
                                                      NonTerminal.ACTUALS,
                                                      TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.ADD): [   TokenType.LEFTPARENT,
                                                        NonTerminal.ACTUALS,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.RIGHTPARENT): [   TokenType.LEFTPARENT,
                                                               NonTerminal.ACTUALS,
                                                               TokenType.RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.THEN): [   TokenType.LEFTPARENT,
                                                        NonTerminal.ACTUALS,
                                                        TokenType.RIGHTPARENT],
    (NonTerminal.FORMAL, TokenType.COLON): [   NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.FORMAL, TokenType.EOF): [],
    (NonTerminal.FORMAL, TokenType.IDENTIFIER): [   NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.FORMALS, TokenType.EOF): [],
    (NonTerminal.LITERAL, TokenType.BOOLEAN): [TokenType.BOOLEAN],
    (NonTerminal.LITERAL, TokenType.NUMBER): [TokenType.NUMBER],
    (NonTerminal.NONEMPTYACTUALS, TokenType.EOF): [   NonTerminal.EXPR,
                                                            NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.RIGHTPARENT): [   NonTerminal.EXPR,
                                                                    NonTerminal.NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.EOF): [],
    (NonTerminal.NONEMPTYFORMALS, TokenType.EOF): [   NonTerminal.FORMAL,
                                                            NonTerminal.NONEMPTYFORMALSREST],
    (NonTerminal.NONEMPTYFORMALS, TokenType.RIGHTPARENT): [   NonTerminal.STATEMENTLIST],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.EOF): [   NonTerminal.FORMAL,
                                                                NonTerminal.NONEMPTYFORMALSREST],
    (NonTerminal.PRINTSTATEMENT, TokenType.LEFTPARENT): [   TokenType.PRINT,
                                                                  TokenType.LEFTPARENT,
                                                                  NonTerminal.EXPR,
                                                                  TokenType.RIGHTPARENT,
                                                                  TokenType.SEMICOLON],
    (NonTerminal.PRINTSTATEMENT, TokenType.PRINT): [   TokenType.PRINT,
                                                             TokenType.LEFTPARENT,
                                                             NonTerminal.EXPR,
                                                             TokenType.RIGHTPARENT,
                                                             TokenType.SEMICOLON],
    (NonTerminal.PRINTSTATEMENT, TokenType.RIGHTPARENT): [   TokenType.PRINT,
                                                                   TokenType.LEFTPARENT,
                                                                   NonTerminal.EXPR,
                                                                   TokenType.RIGHTPARENT,
                                                                   TokenType.SEMICOLON],
    (NonTerminal.PROGRAM, TokenType.EOF): [   TokenType.program,
                                                    TokenType.IDENTIFIER,
                                                    TokenType.LEFTPARENT,
                                                    NonTerminal.FORMALS,
                                                    TokenType.RIGHTPARENT,
                                                    TokenType.SEMICOLON,
                                                    NonTerminal.DEFINITIONS,
                                                    NonTerminal.BODY,
                                                    TokenType.PERIOD],
    (NonTerminal.PROGRAM, TokenType.IDENTIFIER): [   TokenType.program,
                                                           TokenType.IDENTIFIER,
                                                           TokenType.LEFTPARENT,
                                                           NonTerminal.FORMALS,
                                                           TokenType.RIGHTPARENT,
                                                           TokenType.SEMICOLON,
                                                           NonTerminal.DEFINITIONS,
                                                           NonTerminal.BODY,
                                                           TokenType.PERIOD],
    (NonTerminal.PROGRAM, TokenType.LEFTPARENT): [   TokenType.program,
                                                           TokenType.IDENTIFIER,
                                                           TokenType.LEFTPARENT,
                                                           NonTerminal.FORMALS,
                                                           TokenType.RIGHTPARENT,
                                                           TokenType.SEMICOLON,
                                                           NonTerminal.DEFINITIONS,
                                                           NonTerminal.BODY,
                                                           TokenType.PERIOD],
    (NonTerminal.PROGRAM, TokenType.PERIOD): [   TokenType.IDENTIFIER,
                                                       TokenType.LEFTPARENT,
                                                       NonTerminal.FORMALS,
                                                       TokenType.RIGHTPARENT,
                                                       TokenType.SEMICOLON,
                                                       NonTerminal.DEFINITIONS,
                                                       NonTerminal.BODY,
                                                       TokenType.PERIOD],
    (NonTerminal.PROGRAM, TokenType.RIGHTPARENT): [   TokenType.program,
                                                            TokenType.IDENTIFIER,
                                                            TokenType.LEFTPARENT,
                                                            NonTerminal.FORMALS,
                                                            TokenType.RIGHTPARENT,
                                                            TokenType.SEMICOLON,
                                                            NonTerminal.DEFINITIONS,
                                                            NonTerminal.BODY,
                                                            TokenType.PERIOD],
    (NonTerminal.PROGRAM, TokenType.SEMICOLON): [   TokenType.program,
                                                          TokenType.IDENTIFIER,
                                                          TokenType.LEFTPARENT,
                                                          NonTerminal.FORMALS,
                                                          TokenType.RIGHTPARENT,
                                                          TokenType.SEMICOLON,
                                                          NonTerminal.DEFINITIONS,
                                                          NonTerminal.BODY,
                                                          TokenType.PERIOD],
    (NonTerminal.PROGRAM, TokenType.program): [   TokenType.program,
                                                        TokenType.IDENTIFIER,
                                                        TokenType.LEFTPARENT,
                                                        NonTerminal.FORMALS,
                                                        TokenType.RIGHTPARENT,
                                                        TokenType.SEMICOLON,
                                                        NonTerminal.DEFINITIONS,
                                                        NonTerminal.BODY,
                                                        TokenType.PERIOD],
    (NonTerminal.SEPRIME, TokenType.EOF): [],
    (NonTerminal.SEPRIME, TokenType.SUBTRACT): [   TokenType.SUBTRACT,
                                                      NonTerminal.TERM],
    (NonTerminal.SEPRIME, TokenType.OR): [   TokenType.OR,
                                                   NonTerminal.TERM],
    (NonTerminal.SEPRIME, TokenType.ADD): [   TokenType.ADD,
                                                     NonTerminal.TERM],
    (NonTerminal.SIMPLEEXPR, TokenType.ELSE): [   NonTerminal.TERM,
                                                        NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.END): [   NonTerminal.TERM,
                                                       NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.EOF): [   NonTerminal.TERM,
                                                       NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.EQUAL): [   NonTerminal.TERM,
                                                         NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.LESS): [   NonTerminal.TERM,
                                                        NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.RIGHTPARENT): [   NonTerminal.TERM,
                                                               NonTerminal.SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.THEN): [   NonTerminal.TERM,
                                                        NonTerminal.SEPRIME],
    (NonTerminal.STATEMENTLIST, TokenType.RETURN): [   TokenType.RETURN,
                                                             NonTerminal.EXPR],
    (NonTerminal.TERM, TokenType.ELSE): [   NonTerminal.FACTOR,
                                                  NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.END): [   NonTerminal.FACTOR,
                                                 NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.EOF): [   NonTerminal.FACTOR,
                                                 NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.EQUAL): [   NonTerminal.FACTOR,
                                                   NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.LESS): [   NonTerminal.FACTOR,
                                                  NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.SUBTRACT): [   NonTerminal.FACTOR,
                                                   NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.ADD): [   NonTerminal.FACTOR,
                                                  NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.RIGHTPARENT): [   NonTerminal.FACTOR,
                                                         NonTerminal.TERMPRIME],
    (NonTerminal.TERM, TokenType.THEN): [   NonTerminal.FACTOR,
                                                  NonTerminal.TERMPRIME],
    (NonTerminal.TERMPRIME, TokenType.AND): [   TokenType.AND,
                                                      NonTerminal.FACTOR],
    (NonTerminal.TERMPRIME, TokenType.DIVIDE): [   TokenType.DIVIDE,
                                                         NonTerminal.FACTOR],
    (NonTerminal.TERMPRIME, TokenType.EOF): [],
    (NonTerminal.TERMPRIME, TokenType.MULTIPLY): [   TokenType.MULTIPLY,
                                                           NonTerminal.FACTOR],
    (NonTerminal.TYPE, TokenType.BOOLEAN): [TokenType.BOOLEAN],
    (NonTerminal.TYPE, TokenType.NUMBER): [TokenType.NUMBER]}


#Parser 
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        
    def parse(self):
        parseStack = []
        semanticStack = []
        push_rule([TokenType.program, TokenType.EOF], parseStack)
        while parseStack:
            grammarRule = top(parseStack)
            print(grammarRule)
            if isinstance( grammarRule, TokenType):
                t = self.scanner.next_token()
                if grammarRule == t.token_type:
                    pop(parseStack)
                else:
                    msg ='token mismatch: {} and {}'
                    raise ParseError(msg.format(grammarRule,t))
            elif isinstance( grammarRule, NonTerminal):
                t = self.scanner.peek()
                rule = parse_table.get( (grammarRule, t.token_type))
                if rule is not None:
                    pop(parseStack)
                    push_rule(rule, ParseStack)
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
