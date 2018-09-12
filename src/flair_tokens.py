from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    IDENTIFIER = 2
    BOOLEAN = 3

    #Mathematical Operations
    ADD = 4
    SUBTRACT = 5
    MULTIPLY = 6
    DIVIDE = 7
    GREATER = 8
    LESS = 9
    EQUAL = 10
    
    #Punctuators
    LEFTBRACKET = 11
    RIGHTBRACKET = 12
    COMMA = 13
    SEMICOLON = 14
    COLON = 15
    PERIOD = 16
    LEFTPARENT = 17
    RIGHTPARENT = 18

    EOF = 19

class Token:
    def __init__(self, token_type, token_value = None):
        self.token_type = token_type
        self.token_value = token_value

    def value(self):
        return self.token_value

    def is_number(self):
        return self.token_type == TokenType.NUMBER

    def is_identifier(self):
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

    def is_greater(self):
        return self.token_type == TokenType.GREATER

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

    def is_eof(self):
        return self.token_type == TokenType.EOF


    def __repr__(self):
        if self.is_number():
            return 'number = ' + str(self.token_value)
        elif self.is_identifier():
            return 'identifier = ' + self.token_value
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
        elif self.is_greater():
            return 'greater than'
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
        else: #self.is_eof():
            return 'end_of_file'

