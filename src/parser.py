#parser.py
#table driven parser for flair

from scanner import Scanner
from error   import ParseError, SemanticError
#import Non-Terminal tokens enum, Terminal tokens enum, AST Stack/Node creation functions, AST action_table, and parse_table 
from tables import * 


#Parser 
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        
    def parse(self):
        #Initialize empty lists for parse stack and semantic action stack
        tokenCount = 0
        parseStack = []
        semanticStack = []

        #push the first rule to the stack
        push_rule([NonTerminal.PROGRAM, TokenType.EOF], parseStack)
        
        while parseStack:
            #grammarRule is any item in the parse stack, specifically, the top item
            grammarRule = top(parseStack)
            
            #check what the top item (grammarRule) is
            if isinstance( grammarRule, TokenType):
                t = self.scanner.next()
                tokenCount += 1
                if grammarRule == t.token_type:
                    #if the terminal token is a Terminal Token with a value, store the value in the AST stack
                    if t.is_number() or t.is_boolean() or t.is_word():
                        push(t.value(), semanticStack)
                    #pop the Terminal Token
                    pop(parseStack)
                else:
                    msg ='token mismatch: expected {} got {}'
                    raise ParseError(msg.format(grammarRule,t))
            
            #if the top of the stack is a NonTerminal Token        
            elif isinstance( grammarRule, NonTerminal):
                t = self.scanner.peek()
                #lookup expansion in the parse_table
                rule = parse_table.get( (grammarRule, t.token_type))
                #if the expansion exists, add the tokens to the parse stack
                if rule != None:
                    pop(parseStack)
                    push_rule(rule, parseStack)
                else:
                    msg = 'cannot expand {} on {}'
                    raise ParseError(msg.format(grammarRule,t))
            #if the top of the parse stack is an AST action, do the action
            elif isinstance(grammarRule, Ast_Type):
                actionNode = action_table.get(grammarRule) #lookup function to create node
                actionNode(semanticStack) #call function to create node
                pop(parseStack) #pop semantic action from parse stack
            else:
                msg = 'invalid item on stack: {}'
                raise ParseError(msg.format(grammarRule))
                    
        if not t.is_eof():
            msg = 'unexpected token at end: {}'
            raise ParseError(msg.format(t))
        
        #The items in the semanticStack get condensed into a single program node, which can be printed
        return semanticStack[0]
