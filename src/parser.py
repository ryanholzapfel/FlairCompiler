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
    NONEMPTYFORMALS-REST    = 6               
    BODY                    = 7
    STATEMENT-LIST          = 8       
    TYPE                    = 9
    EXPR                    = 10
    EXPR-PRIME              = 11  
    SIMPLE-EXPR             = 12    
    SE-PRIME                = 13
    TERM                    = 14
    TERM-PRIME              = 15  
    FACTOR                  = 16
    FACTOR-REST             = 17      
    ACTUALS                 = 18
    NONEMPTYACTUALS         = 19      
    NONEMPTYACTUALS-REST    = 20        
    LITERAL                 = 21
    PRINT-STATEMENT         = 22      
    
#Stack Operations
def top(stack):
    return stack[-1]

def pop(stack):
    stack.pop()

def push_rule(lst, stack):
    for element in reversed(lst):
        stack.append(element)


#parse table
parse_table = {   (NonTerminal.ACTUALS, TokenType.$): [],
    (NonTerminal.BODY, TokenType.BEGIN): [   BEGIN,
                                                   STATEMENTLIST,
                                                   END],
    (NonTerminal.BODY, TokenType.END): [   BEGIN,
                                                 STATEMENTLIST,
                                                 END],
    (NonTerminal.DEF, TokenType.COLON): [   FUNCTION,
                                                  IDENTIFIER,
                                                  LEFTPARENT,
                                                  FORMALS,
                                                  RIGHTPARENT,
                                                  COLON,
                                                  TYPEBODY,
                                                  SEMICOLON],
    (NonTerminal.DEF, TokenType.FUNCTION): [   FUNCTION,
                                                     IDENTIFIER,
                                                     LEFTPARENT,
                                                     FORMALS,
                                                     RIGHTPARENT,
                                                     COLON,
                                                     TYPEBODY,
                                                     SEMICOLON],
    (NonTerminal.DEF, TokenType.IDENTIFIER): [   FUNCTION,
                                                       IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       COLON,
                                                       TYPEBODY,
                                                       SEMICOLON],
    (NonTerminal.DEF, TokenType.LEFTPARENT): [   FUNCTION,
                                                       IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       COLON,
                                                       TYPEBODY,
                                                       SEMICOLON],
    (NonTerminal.DEF, TokenType.RIGHTPARENT): [   FUNCTION,
                                                        IDENTIFIER,
                                                        LEFTPARENT,
                                                        FORMALS,
                                                        RIGHTPARENT,
                                                        COLON,
                                                        TYPEBODY,
                                                        SEMICOLON],
    (NonTerminal.DEF, TokenType.SEMICOLON): [   FUNCTION,
                                                      IDENTIFIER,
                                                      LEFTPARENT,
                                                      FORMALS,
                                                      RIGHTPARENT,
                                                      COLON,
                                                      TYPEBODY,
                                                      SEMICOLON],
    (NonTerminal.DEFINITIONS, TokenType.$): [],
    (NonTerminal.DEFINITIONS, TokenType.BEGIN): [   DEF,
                                                          DEFINITIONS],
    (NonTerminal.EXPR, TokenType.$): [SIMPLEEXPR, EXPRPRIME],
    (NonTerminal.EXPR, TokenType.ELSE): [SIMPLEEXPR, EXPRPRIME],
    (NonTerminal.EXPR, TokenType.END): [SIMPLEEXPR, EXPRPRIME],
    (NonTerminal.EXPR, TokenType.RIGHTPARENT): [   SIMPLEEXPR,
                                                         EXPRPRIME],
    (NonTerminal.EXPR, TokenType.THEN): [SIMPLEEXPR, EXPRPRIME],
    (NonTerminal.EXPRPRIME, TokenType.$): [],
    (NonTerminal.EXPRPRIME, TokenType.EQUAL): [EQUAL, SIMPLEEXPR],
    (NonTerminal.EXPRPRIME, TokenType.LESS): [LESS, SIMPLEEXPR],
    (NonTerminal.FACTOR, TokenType.$): [IDENTIFIER, FACTORREST],
    (NonTerminal.FACTOR, TokenType.DIVIDE): [   LEFTPARENT,
                                                      EXPR,
                                                      RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.ELSE): [   IF,
                                                    EXPR,
                                                    THEN,
                                                    EXPR,
                                                    ELSE,
                                                    EXPR],
    (NonTerminal.FACTOR, TokenType.EQUAL): [   LEFTPARENT,
                                                     EXPR,
                                                     RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.IDENTIFIER): [   IDENTIFIER,
                                                          FACTORREST],
    (NonTerminal.FACTOR, TokenType.IF): [   IF,
                                                  EXPR,
                                                  THEN,
                                                  EXPR,
                                                  ELSE,
                                                  EXPR],
    (NonTerminal.FACTOR, TokenType.LESS): [   LEFTPARENT,
                                                    EXPR,
                                                    RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.MINUS): [MINUS, FACTOR],
    (NonTerminal.FACTOR, TokenType.MULTIPLY): [   LEFTPARENT,
                                                        EXPR,
                                                        RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.NOT): [NOT, FACTOR],
    (NonTerminal.FACTOR, TokenType.PLUS): [   LEFTPARENT,
                                                    EXPR,
                                                    RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.RIGHTPARENT): [   LEFTPARENT,
                                                           EXPR,
                                                           RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.THEN): [   IF,
                                                    EXPR,
                                                    THEN,
                                                    EXPR,
                                                    ELSE,
                                                    EXPR],
    (NonTerminal.FACTORREST, TokenType.$): [],
    (NonTerminal.FACTORREST, TokenType.AND): [   LEFTPARENT,
                                                       ACTUALS,
                                                       RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.DIVIDE): [   LEFTPARENT,
                                                          ACTUALS,
                                                          RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.ELSE): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.END): [   LEFTPARENT,
                                                       ACTUALS,
                                                       RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.EQUAL): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.LEFTPARENT): [   LEFTPARENT,
                                                              ACTUALS,
                                                              RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.LESS): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.MINUS): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.MULTIPLY): [   LEFTPARENT,
                                                            ACTUALS,
                                                            RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.OR): [   LEFTPARENT,
                                                      ACTUALS,
                                                      RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.PLUS): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.RIGHTPARENT): [   LEFTPARENT,
                                                               ACTUALS,
                                                               RIGHTPARENT],
    (NonTerminal.FACTORREST, TokenType.THEN): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FORMAL, TokenType.$): [],
    (NonTerminal.FORMAL, TokenType.COLON): [NONEMPTYFORMALS],
    (NonTerminal.FORMAL, TokenType.IDENTIFIER): [NONEMPTYFORMALS],
    (NonTerminal.FORMALS, TokenType.$): [],
    (NonTerminal.LITERAL, TokenType.BOOLEAN): [BOOLEAN],
    (NonTerminal.LITERAL, TokenType.NUMBER): [NUMBER],
    (NonTerminal.NONEMPTYACTUALS, TokenType.$): [   EXPR,
                                                          NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.RIGHTPARENT): [   EXPR,
                                                                    NONEMPTYACTUALSREST],
    (NonTerminal.NONEMPTYACTUALSREST, TokenType.$): [],
    (NonTerminal.NONEMPTYFORMALS, TokenType.$): [   FORMAL,
                                                          NONEMPTYFORMALSREST],
    (NonTerminal.NONEMPTYFORMALS, TokenType.RIGHTPARENT): [   STATEMENTLIST],
    (NonTerminal.NONEMPTYFORMALSREST, TokenType.$): [   FORMAL,
                                                              NONEMPTYFORMALSREST],
    (NonTerminal.PRINTSTATEMENT, TokenType.LEFTPARENT): [   PRINT,
                                                                  LEFTPARENT,
                                                                  EXPR,
                                                                  RIGHTPARENT,
                                                                  SEMICOLON],
    (NonTerminal.PRINTSTATEMENT, TokenType.PRINT): [   PRINT,
                                                             LEFTPARENT,
                                                             EXPR,
                                                             RIGHTPARENT,
                                                             SEMICOLON],
    (NonTerminal.PRINTSTATEMENT, TokenType.RIGHTPARENT): [   PRINT,
                                                                   LEFTPARENT,
                                                                   EXPR,
                                                                   RIGHTPARENT,
                                                                   SEMICOLON],
    (NonTerminal.PROGRAM, TokenType.$): [   program,
                                                  IDENTIFIER,
                                                  LEFTPARENT,
                                                  FORMALS,
                                                  RIGHTPARENT,
                                                  SEMICOLONDEFINITIONSBODY,
                                                  PERIOD],
    (NonTerminal.PROGRAM, TokenType.IDENTIFIER): [   program,
                                                           IDENTIFIER,
                                                           LEFTPARENT,
                                                           FORMALS,
                                                           RIGHTPARENT,
                                                           SEMICOLONDEFINITIONSBODY,
                                                           PERIOD],
    (NonTerminal.PROGRAM, TokenType.LEFTPARENT): [   program,
                                                           IDENTIFIER,
                                                           LEFTPARENT,
                                                           FORMALS,
                                                           RIGHTPARENT,
                                                           SEMICOLONDEFINITIONSBODY,
                                                           PERIOD],
    (NonTerminal.PROGRAM, TokenType.PERIOD): [   IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       SEMICOLONDEFINITIONSBODY,
                                                       PERIOD],
    (NonTerminal.PROGRAM, TokenType.RIGHTPARENT): [   program,
                                                            IDENTIFIER,
                                                            LEFTPARENT,
                                                            FORMALS,
                                                            RIGHTPARENT,
                                                            SEMICOLONDEFINITIONSBODY,
                                                            PERIOD],
    (NonTerminal.PROGRAM, TokenType.SEMICOLON): [   program,
                                                          IDENTIFIER,
                                                          LEFTPARENT,
                                                          FORMALS,
                                                          RIGHTPARENT,
                                                          SEMICOLONDEFINITIONSBODY,
                                                          PERIOD],
    (NonTerminal.PROGRAM, TokenType.program): [   program,
                                                        IDENTIFIER,
                                                        LEFTPARENT,
                                                        FORMALS,
                                                        RIGHTPARENT,
                                                        SEMICOLONDEFINITIONSBODY,
                                                        PERIOD],
    (NonTerminal.SEPRIME, TokenType.$): [],
    (NonTerminal.SEPRIME, TokenType.MINUS): [MINUS, TERM],
    (NonTerminal.SEPRIME, TokenType.OR): [OR, TERM],
    (NonTerminal.SEPRIME, TokenType.PLUS): [PLUS, TERM],
    (NonTerminal.SIMPLEEXPR, TokenType.$): [TERM, SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.ELSE): [TERM, SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.END): [TERM, SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.EQUAL): [TERM, SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.LESS): [TERM, SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.RIGHTPARENT): [   TERM,
                                                               SEPRIME],
    (NonTerminal.SIMPLEEXPR, TokenType.THEN): [TERM, SEPRIME],
    (NonTerminal.STATEMENTLIST, TokenType.RETURN): [RETURN, EXPR],
    (NonTerminal.TERM, TokenType.$): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.ELSE): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.END): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.EQUAL): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.LESS): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.MINUS): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.PLUS): [FACTOR, TERMPRIME],
    (NonTerminal.TERM, TokenType.RIGHTPARENT): [   FACTOR,
                                                         TERMPRIME],
    (NonTerminal.TERM, TokenType.THEN): [FACTOR, TERMPRIME],
    (NonTerminal.TERMPRIME, TokenType.$): [],
    (NonTerminal.TERMPRIME, TokenType.AND): [AND, FACTOR],
    (NonTerminal.TERMPRIME, TokenType.DIVIDE): [DIVIDE, FACTOR],
    (NonTerminal.TERMPRIME, TokenType.MULTIPLY): [MULTIPLY, FACTOR],
    (NonTerminal.TYPE, TokenType.BOOLEAN): [BOOLEAN],
    (NonTerminal.TYPE, TokenType.NUMBER): [NUMBER]}


#Parser 
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        
    def parse(self):
        parseStack = []
        semanticStack = []
        push_rule([Nonterminal.Program, TokenType.EOF], parseStack)
        while parseStack:
            grammarRule = top(parseStack)
            if isinstance( grammarRule, TokenType):
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
