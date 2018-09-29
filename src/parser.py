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
parse_table = {   (NonTerminal.ACTUALS, TokenType.EOF): [ε],
    (NonTerminal.BODY, TokenType.begin): [   begin,
                                                   STATEMENT-LIST,
                                                   end],
    (NonTerminal.BODY, TokenType.end): [   begin,
                                                 STATEMENT-LIST,
                                                 end],
    (NonTerminal.DEF, TokenType.COLON): [   function,
                                                  IDENTIFIER,
                                                  LEFTPARENT,
                                                  FORMALS,
                                                  RIGHTPARENT,
                                                  COLON,
                                                  TYPEBODY,
                                                  SEMICOLON],
    (NonTerminal.DEF, TokenType.LEFTPARENT): [   function,
                                                       IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       COLON,
                                                       TYPEBODY,
                                                       SEMICOLON],
    (NonTerminal.DEF, TokenType.RIGHTPARENT): [   function,
                                                        IDENTIFIER,
                                                        LEFTPARENT,
                                                        FORMALS,
                                                        RIGHTPARENT,
                                                        COLON,
                                                        TYPEBODY,
                                                        SEMICOLON],
    (NonTerminal.DEF, TokenType.SEMICOLON): [   function,
                                                      IDENTIFIER,
                                                      LEFTPARENT,
                                                      FORMALS,
                                                      RIGHTPARENT,
                                                      COLON,
                                                      TYPEBODY,
                                                      SEMICOLON],
    (NonTerminal.DEF, TokenType.function): [   function,
                                                     IDENTIFIER,
                                                     LEFTPARENT,
                                                     FORMALS,
                                                     RIGHTPARENT,
                                                     COLON,
                                                     TYPEBODY,
                                                     SEMICOLON],
    (NonTerminal.DEF, TokenType.identifier): [   function,
                                                       IDENTIFIER,
                                                       LEFTPARENT,
                                                       FORMALS,
                                                       RIGHTPARENT,
                                                       COLON,
                                                       TYPEBODY,
                                                       SEMICOLON],
    (NonTerminal.DEFINITIONS, TokenType.EOF): [ε],
    (NonTerminal.DEFINITIONS, TokenType.begin): [   DEF,
                                                          DEFINITIONS],
    (NonTerminal.EXPR-PRIME, TokenType.EOF): [ε],
    (NonTerminal.EXPR-PRIME, TokenType.EQUAL): [EQUAL, SIMPLE-EXPR],
    (NonTerminal.EXPR-PRIME, TokenType.LESS): [LESS, SIMPLE-EXPR],
    (NonTerminal.EXPR, TokenType.EOF): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.RIGHTPARENT): [   SIMPLE-EXPR,
                                                         EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.else): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.end): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.EXPR, TokenType.then): [SIMPLE-EXPR, EXPR-PRIME],
    (NonTerminal.FACTOR-REST, TokenType.EOF): [ε],
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
    (NonTerminal.FACTOR-REST, TokenType.and): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.else): [   LEFTPARENT,
                                                         ACTUALS,
                                                         RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.end): [   LEFTPARENT,
                                                        ACTUALS,
                                                        RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.or): [   LEFTPARENT,
                                                       ACTUALS,
                                                       RIGHTPARENT],
    (NonTerminal.FACTOR-REST, TokenType.then): [   LEFTPARENT,
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
    (NonTerminal.FACTOR, TokenType.else): [   if,
                                                    EXPR,
                                                    then,
                                                    EXPR,
                                                    else,
                                                    EXPR],
    (NonTerminal.FACTOR, TokenType.identifier): [   IDENTIFIER,
                                                          FACTOR-REST],
    (NonTerminal.FACTOR, TokenType.if): [   if,
                                                  EXPR,
                                                  then,
                                                  EXPR,
                                                  else,
                                                  EXPR],
    (NonTerminal.FACTOR, TokenType.not): [not, FACTOR],
    (NonTerminal.FACTOR, TokenType.then): [   if,
                                                    EXPR,
                                                    then,
                                                    EXPR,
                                                    else,
                                                    EXPR],
    (NonTerminal.FORMAL, TokenType.EOF): [ε],
    (NonTerminal.FORMAL, TokenType.COLON): [NONEMPTYFORMALS],
    (NonTerminal.FORMAL, TokenType.identifier): [NONEMPTYFORMALS],
    (NonTerminal.FORMALS, TokenType.EOF): [ε],
    (NonTerminal.LITERAL, TokenType.NUMBER): [NUMBER],
    (NonTerminal.LITERAL, TokenType.boolean): [BOOLEAN],
    (NonTerminal.NONEMPTYACTUALS-REST, TokenType.EOF): [ε],
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
    (NonTerminal.PROGRAM, TokenType.identifier): [   program,
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
    (NonTerminal.SE-PRIME, TokenType.EOF): [ε],
    (NonTerminal.SE-PRIME, TokenType.MINUS): [MINUS, TERM],
    (NonTerminal.SE-PRIME, TokenType.PLUS): [PLUS, TERM],
    (NonTerminal.SE-PRIME, TokenType.or): [or, TERM],
    (NonTerminal.SIMPLE-EXPR, TokenType.EOF): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.EQUAL): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.LESS): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.RIGHTPARENT): [   TERM,
                                                                SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.else): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.end): [TERM, SE-PRIME],
    (NonTerminal.SIMPLE-EXPR, TokenType.then): [TERM, SE-PRIME],
    (NonTerminal.STATEMENT-LIST, TokenType.return): [return, EXPR],
    (NonTerminal.TERM-PRIME, TokenType.EOF): [ε],
    (NonTerminal.TERM-PRIME, TokenType.DIVIDE): [DIVIDE, FACTOR],
    (NonTerminal.TERM-PRIME, TokenType.MULTIPLY): [   MULTIPLY,
                                                            FACTOR],
    (NonTerminal.TERM-PRIME, TokenType.and): [and, FACTOR],
    (NonTerminal.TERM, TokenType.EOF): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.EQUAL): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.LESS): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.MINUS): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.PLUS): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.RIGHTPARENT): [   FACTOR,
                                                         TERM-PRIME],
    (NonTerminal.TERM, TokenType.else): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.end): [FACTOR, TERM-PRIME],
    (NonTerminal.TERM, TokenType.then): [FACTOR, TERM-PRIME],
    (NonTerminal.TYPE, TokenType.NUMBER): [NUMBER],
    (NonTerminal.TYPE, TokenType.boolean): [boolean]}


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
