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
    NONEMPTYFORMALS-REST
    BODY = 6
    STATEMENT-LIST = 7
    TYPE = 8
    EXPR = 9
    EXPR-PRIME = 10
    SIMPLE-EXPR = 11
    SE-PRIME = 12
    TERM = 13
    TERM-PRIME = 14
    FACTOR = 15
    FACTOR-REST = 16
    ACTUALS = 17
    NONEMPTYACTUALS = 18
    NONEMPTYACTUALS-REST = 19
    LITERAL = 20
    PRINT-STATEMENT = 21
    
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
    (NonTerminal.BODY, TokenType.BEGIN): [BEGIN,
                                                   STATEMENT-LIST,
                                                   END],
    (NonTerminal.BODY, TokenType.END): [   BEGIN,
                                                 STATEMENT-LIST,
                                                 END],
    (NonTerminal.DEF, TokenType.COLON): [   FUNCTION,
                                                  IDENTIFIER,
                                                  LEFTPARENT,
                                                  FORMALS,
                                                  RIGHTPARENT,
                                                  COLON,
                                                  TYPE,BODY,
                                                  SEMICOLON],
    (NonTerminal.DEF, TokenType.LEFTPARENT): [   FUNCTION,
                                                       IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       COLON,
                                                       TYPE,BODY,
                                                       SEMICOLON],
    (NonTerminal.DEF, TokenType.RIGHTPARENT): [   FUNCTION,
                                                        IDENTIFIER,
                                                        LEFTPARENT,
                                                        FORMALS,
                                                        RIGHTPARENT,
                                                        COLON,
                                                        TYPE,BODY,
                                                        SEMICOLON],
    (NonTerminal.DEF, TokenType.SEMICOLON): [   FUNCTION,
                                                      IDENTIFIER,
                                                      LEFTPARENT,
                                                      FORMALS,
                                                      RIGHTPARENT,
                                                      COLON,
                                                      TYPE,BODY,
                                                      SEMICOLON],
    (NonTerminal.DEF, TokenType.FUNCTION): [   FUNCTION,
                                                     IDENTIFIER,
                                                     LEFTPARENT,
                                                     FORMALS,
                                                     RIGHTPARENT,
                                                     COLON,
                                                     TYPE,BODY,
                                                     SEMICOLON],
    (NonTerminal.DEF, TokenType.IDENTIFIER): [   FUNCTION,
                                                       IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       COLON,
                                                       TYPE,BODY,
                                                       SEMICOLON],
    (NonTerminal.DEFINITIONS, TokenType.EOF): [],
    (NonTerminal.DEFINITIONS, TokenType.BEGIN): [   DEF,
                                                          DEFINITIONS],
    (NonTerminal.EXPR-PRIME, TokenType.EOF): [],
    (NonTerminal.EXPR-PRIME, TokenType.EQUAL): [EQUAL, SIMPLE-EXPR],
    (NonTerminal.EXPR-PRIME, TokenType.LESS): [LESS, SIMPLE-EXPR],
    (NonTerminal.EXPR, TokenType.EOF): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.RIGHTPARENT): [   SIMPLE-EXPR,
                                                         EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.ELSE): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.END): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.THEN): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.FACTOR-REST, TokenType.EOF): [],
    (NonTerminal.FACTOR-REST, TokenType.DIVIDE): [   LEFTPARENT,
                                                           ACTUALS,
                                                           RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.EQUAL): [   LEFTPARENT,
                                                          ACTUALS,
                                                          RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.LEFTPARENT): [   LEFTPARENT,
                                                               ACTUALS,
                                                               RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.LESS): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.MINUS): [   LEFTPARENT,
                                                          ACTUALS,
                                                          RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.MULTIPLY): [   LEFTPARENT,
                                                             ACTUALS,
                                                             RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.PLUS): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.RIGHTPARENT): [   LEFTPARENT,
                                                                ACTUALS,
                                                                RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.AND): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.ELSE): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.END): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.OR): [   LEFTPARENT,
                                                       ACTUALS,
                                                       RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.THEN): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.EOF): [IDENTIFIER, FACTOR-REST],
    (NonTerminal.FACTOR, TokenType.DIVIDE): [   LEFTPARENT,
                                                      EXPR,
                                                      RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.EQUAL): [   LEFTPARENT,
                                                     EXPR,
                                                     RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.LESS): [   LEFTPARENT,
                                                    EXPR,
                                                    RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.MINUS): [MINUS, FACTOR],
    (NonTerminal.FACTOR, TokenType.MULTIPLY): [   LEFTPARENT,
                                                        EXPR,
                                                        RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.PLUS): [   LEFTPARENT,
                                                    EXPR,
                                                    RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.RIGHTPARENT): [   LEFTPARENT,
                                                           EXPR,
                                                           RIGHTPARENT],
    (NonTerminal.FACTOR, TokenType.ELSE): [   IF,
                                                    EXPR,
                                                    THEN,
                                                    EXPR,
                                                    ELSE,
                                                    EXPR],
    (NonTerminal.FACTOR, TokenType.IDENTIFIER): [   IDENTIFIER,
                                                          FACTOR-REST],
    (NonTerminal.FACTOR, TokenType.IF): [   IF,
                                                  EXPR,
                                                  THEN,
                                                  EXPR,
                                                  ELSE,
                                                  EXPR],
    (NonTerminal.FACTOR, TokenType.NOT): [NOT, FACTOR],
    (NonTerminal.FACTOR, TokenType.THEN): [   IF,
                                                    EXPR,
                                                    THEN,
                                                    EXPR,
                                                    ELSE,
                                                    EXPR],
    (NonTerminal.FORMAL, TokenType.EOF): [],
    (NonTerminal.FORMAL, TokenType.COLON): [NONEMPTYFORMALS],
    (NonTerminal.FORMAL, TokenType.IDENTIFIER): [NONEMPTYFORMALS],
    (NonTerminal.FORMALS, TokenType.EOF): [],
    (NonTerminal.LITERAL, TokenType.NUMBER): [NUMBER],
    (NonTerminal.LITERAL, TokenType.BOOLEAN): [BOOLEAN],
    (NonTerminal.NONEMPTYACTUALS-REST, TokenType.EOF): [],
    (NonTerminal.NONEMPTYACTUALS, TokenType.EOF): [   EXPR,
                                                          NONEMPTYACTUALS-REST],
    (NonTerminal.NONEMPTYACTUALS, TokenType.RIGHTPARENT): [   EXPR,
                                                                    NONEMPTYACTUALS-REST],
    (NonTerminal.NONEMPTYFORMALS-REST, TokenType.EOF): [   FORMAL,
                                                               NONEMPTYFORMALS-REST],
    (NonTerminal.NONEMPTYFORMALS, TokenType.EOF): [   FORMAL,
                                                          NONEMPTYFORMALS-REST],
    (NonTerminal.NONEMPTYFORMALS, TokenType.RIGHTPARENT): [   FORMAL,
                                                                    NONEMPTYFORMALS-REST],
    (NonTerminal.PRINT-STATEMENT, TokenType.LEFTPARENT): [   print,
                                                                   LEFTPARENT,
                                                                   EXPR,
                                                                   RIGHTPARENT,
                                                                   SEMICOLON],
    (NonTerminal.PRINT-STATEMENT, TokenType.RIGHTPARENT): [   print,
                                                                    LEFTPARENT,
                                                                    EXPR,
                                                                    RIGHTPARENT,
                                                                    SEMICOLON],
    (NonTerminal.PRINT-STATEMENT, TokenType.print): [   print,
                                                              LEFTPARENT,
                                                              EXPR,
                                                              RIGHTPARENT,
                                                              SEMICOLON],
    (NonTerminal.PROGRAM, TokenType.EOF): [   program,
                                                  IDENTIFIER,
                                                  LEFTPARENT,
                                                  FORMALS,
                                                  RIGHTPARENT,
                                                  SEMICOLON,DEFINITIONS,BODY,
                                                  PERIOD],
    (NonTerminal.PROGRAM, TokenType.LEFTPARENT): [   program,
                                                           IDENTIFIER,
                                                           LEFTPARENT,
                                                           FORMALS,
                                                           RIGHTPARENT,
                                                           SEMICOLON,DEFINITIONS,BODY,
                                                           PERIOD],
    (NonTerminal.PROGRAM, TokenType.PERIOD): [   IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       SEMICOLON,DEFINITIONS,BODY,
                                                       PERIOD],
    (NonTerminal.PROGRAM, TokenType.RIGHTPARENT): [   program,
                                                            IDENTIFIER,
                                                            LEFTPARENT,
                                                            FORMALS,
                                                            RIGHTPARENT,
                                                            SEMICOLON,DEFINITIONS,BODY,
                                                            PERIOD],
    (NonTerminal.PROGRAM, TokenType.SEMICOLON): [   program,
                                                          IDENTIFIER,
                                                          LEFTPARENT,
                                                          FORMALS,
                                                          RIGHTPARENT,
                                                          SEMICOLON,DEFINITIONS,BODY,
                                                          PERIOD],
    (NonTerminal.PROGRAM, TokenType.IDENTIFIER): [   program,
                                                           IDENTIFIER,
                                                           LEFTPARENT,
                                                           FORMALS,
                                                           RIGHTPARENT,
                                                           SEMICOLON,DEFINITIONS,BODY,
                                                           PERIOD],
    (NonTerminal.PROGRAM, TokenType.program): [   program,
                                                        IDENTIFIER,
                                                        LEFTPARENT,
                                                        FORMALS,
                                                        RIGHTPARENT,
                                                        SEMICOLON,DEFINITIONS,BODY,
                                                        PERIOD],
    (NonTerminal.SE-PRIME, TokenType.EOF): [],
    (NonTerminal.SE-PRIME, TokenType.MINUS): [MINUS, TERM],
    (NonTerminal.SE-PRIME, TokenType.PLUS): [PLUS, TERM],
    (NonTerminal.SE-PRIME, TokenType.OR): [OR, TERM],
    (NonTerminal.SIMPLE-EXPR, TokenType.EOF): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.EQUAL): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.LESS): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.RIGHTPARENT): [   TERM,
                                                                SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.ELSE): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.END): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.THEN): [TERM, SE-PRIME],
    (NonTerminal.STATEMENT-LIST, TokenType.RETURN): [RETURN, EXPR],
    (NonTerminal.TERM-PRIME, TokenType.EOF): [],
    (NonTerminal.TERM-PRIME, TokenType.DIVIDE): [DIVIDE, FACTOR],
    (NonTerminal.TERM-PRIME, TokenType.MULTIPLY): [   MULTIPLY,
                                                            FACTOR],
    (NonTerminal.TERM-PRIME, TokenType.AND): [and, FACTOR],
    (NonTerminal.TERM, TokenType.EOF): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.EQUAL): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.LESS): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.MINUS): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.PLUS): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.RIGHTPARENT): [   FACTOR,
                                                         TERM-PRIME],
    (NonTerminal.TERM, TokenType.ELSE): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.END): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.THEN): [FACTOR, TERM-PRIME],
    (NonTerminal.TYPE, TokenType.NUMBER): [NUMBER],
    (NonTerminal.TYPE, TokenType.BOOLEAN): [BOOLEAN]}


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
