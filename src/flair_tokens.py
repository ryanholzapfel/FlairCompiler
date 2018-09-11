from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    IDENTIFIER = 2
    BOOLEAN = 3
    ADD = 4
    SUBTRACT = 5
    MULTIPLY = 6
    DIVIDE = 7
    GREATER = 8
    LESS = 9
    EQUAL = 10
    PUNCTUATION = 11


class Token:
    def __init__(self, token_type, token_value = None):
        self.token_type = token_type
        self.token_value = token_value

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

    def is_punctuation(self):
        return self.token_type == TokenType.PUNCTUATION

    def __repr__(self):
        if self.is_number():
            return 'number = ' + str(self.token_value))
        elif self.is_word():
            return
