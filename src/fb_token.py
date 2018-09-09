from enum import Enum

class TokenType(Enum):
    ELLIPSIS = 1
    NUMBER   = 2
    EQUALS   = 3
    WORD     = 4
    EOF      = 5

class Token:
    def __init__(self, token_type, token_value = None):
        self.token_type  = token_type
        self.token_value = token_value

    def is_ellipsis(self):
        return self.token_type == TokenType.ELLIPSIS

    def is_number(self):
        return self.token_type == TokenType.NUMBER

    def is_equals(self):
        return self.token_type == TokenType.EQUALS

    def is_word(self):
        return self.token_type == TokenType.WORD

    def is_eof(self):
        return self.token_type == TokenType.EOF

    def value(self):
        return self.token_value
    
    def __repr__(self):
        if self.is_ellipsis():
            return 'ellipsis'
        elif self.is_number():
            return 'number = ' + str(self.token_value)
        elif self.is_equals():
            return 'equal sign'
        elif self.is_word():
            return 'word  = ' + self.token_value
        else:   # is_eof()
            return 'end_of_stream'
