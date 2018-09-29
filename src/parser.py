#parser.py
#table driven parser for flair

from scanner import Scanner

from flair_tokens import Token, TokenType

from error   import ParseError, SemanticError

from enum import Enum

# non-terminals

class NonTerminal(Enum):
    Program     = 0
    Range       = 1
    Assignments = 2
    Assignment  = 3
    Word        = 4
    Number      = 5

#Stack Operations
def top(stack):
    return stack[-1]

def pop(stack):
    stack.pop()

def push_rule(lst, stack):
    for element in reversed(lst):
        stack.append(element)


#parse table

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
