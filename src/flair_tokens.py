from enum import Enum

class TokenType(Enum):
    #Identifiers and data types
    NUMBER = 1
    IDENTIFIER = 2
    BOOLEAN = 3

    #Mathematical Operations
    ADD = 4
    SUBTRACT = 5
    MULTIPLY = 6
    DIVIDE = 7
    LESS = 8
    EQUAL = 9
    
    #Punctuators
    LEFTBRACKET = 10
    RIGHTBRACKET = 11
    COMMA = 12
    SEMICOLON = 13
    COLON = 14
    PERIOD = 15
    LEFTPARENT = 16
    RIGHTPARENT = 17
    EOF = 18
    
    #Keywords
    IF = 19
    THEN = 20
    ELSE = 21
    NOT = 22
    OR = 23
    AND = 24
    PRINT = 25
    BEGIN = 26
    END = 27
    RETURN = 28
    program = 29
    FUNCTION = 30


    

class Token:
    def __init__(self, token_type, token_value = None):
        self.token_type = token_type
        self.token_value = token_value

    def value(self):
        return self.token_value

    def is_number(self):
        return self.token_type == TokenType.NUMBER

    def is_word(self):
        return self.token_type == TokenType.IDENTIFIER

    def is_boolean(self):
        return self.token_type == TokenType.BOOLEAN

    def is_add(self):
        return self.token_type == TokenType.ADD

    def is_subtract(self):
        return self.token_type == TokenType.SUBTRACT

    def is_multiply(self):
        return self.token_type == TokenType.MULTIPLY

    def is_divide(self):
        return self.token_type == TokenType.DIVIDE


    def is_less(self):
        return self.token_type == TokenType.LESS

    def is_equal(self):
        return self.token_type == TokenType.EQUAL

    def is_leftbracket(self):
        return self.token_type == TokenType.LEFTBRACKET
    
    def is_rightbracket(self):
        return self.token_type == TokenType.RIGHTBRACKET

    def is_comma(self):
        return self.token_type == TokenType.COMMA

    def is_semicolon(self):
        return self.token_type == TokenType.SEMICOLON

    def is_period(self):
        return self.token_type == TokenType.PERIOD

    def is_leftparent(self):
        return self.token_type == TokenType.LEFTPARENT

    def is_rightparent(self):
        return self.token_type == TokenType.RIGHTPARENT

    def is_colon(self):
        return self.token_type == TokenType.COLON

    def is_eof(self):
        return self.token_type == TokenType.EOF
    def is_if(self):
    	return self.token_type == TokenType.IF
    def is_then(self):
    	return self.token_type == TokenType.THEN
    def is_else(self):
    	return self.token_type == TokenType.ELSE
    def is_not(self):
    	return self.token_type == TokenType.NOT
    def is_or(self):
    	return self.token_type == TokenType.OR
    def is_and(self):
    	return self.token_type == TokenType.AND
    def is_print(self):
    	return self.token_type == TokenType.PRINT
    def is_begin(self):
    	return self.token_type == TokenType.BEGIN
    def is_end(self):
    	return self.token_type == TokenType.END
    def is_return(self):
    	return self.token_type == TokenType.RETURN
    def is_program(self):
    	return self.token_type == TokenType.program
    def is_function(self):
    	return self.token_type == TokenType.FUNCTION


    def __repr__(self):
        if self.is_number():
            return 'number = ' + str(self.token_value)
        elif self.is_word():
            return 'word = ' + self.token_value
        elif self.is_boolean():
            return 'boolean = ' + str(self.token_value)
        elif self.is_add():
            return 'addition sign'
        elif self.is_subtract():
            return 'subtraction sign'
        elif self.is_multiply():
            return 'multiplication sign'
        elif self.is_divide():
            return 'division sign'
        elif self.is_less():
            return 'less than'
        elif self.is_equal():
            return 'equals sign'
        elif self.is_leftbracket():
            return 'leftbracket'
        elif self.is_rightbracket():
            return 'rightbracket'
        elif self.is_comma():
            return 'comma'
        elif self.is_semicolon():
            return 'semicolon'
        elif self.is_period():
            return 'period'
        elif self.is_leftparent():
            return 'leftparent'
        elif self.is_rightparent():
            return 'rightparent'
        elif self.is_colon():
            return "colon"
        elif self.is_eof():
            return 'end_of_file'
        elif self.is_if():
        	return 'if'
        elif self.is_then():
        	return 'then'
        elif self.is_else():
        	return 'else'
        elif self.is_not():
        	return 'not'
        elif self.is_or():
        	return 'or'
        elif self.is_and():
        	return 'and'
        elif self.is_print():
        	return 'print'
        elif self.is_begin():
        	return 'begin'
        elif self.is_end():
        	return 'end'
        elif self.is_return():
        	return 'return'
        elif self.is_program():
        	return 'program'
        else:# self.is_function():
        	return 'function'
