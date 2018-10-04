from flair_tokens import Token, TokenType
from error   import LexicalError

class Scanner:
  'Read tokens from an input stream'

    def __init__(self, program_str):
        self.program_str = program_str
        self.pos         = 0
        self.lookahead   = None
     
    def peek(self):
        if not self.lookahead:
            self.lookahead = self.get_next_token()
        return self.lookahead
        
    def next_token(self):
        if self.lookahead:
            answer = self.lookahead
            self.lookahead = None
            return answer
        else:
            return self.get_next_token()

  # --------------------------------------------------------
  #checks for valid tolkens returns token types
  #booleans keywords and identifiers to be handled as words 

    def get_next_token(self):
        self.skip_whitespace()
    
    if self.pos >= len(self.program_str):
        return Token(TokenType.EOF)

   # if self.program_str[self.pos:].startswith('...'):
     # self.pos += 3
     # return Token(TokenType.ELLIPSIS)

    if self.program_str[self.pos].isalpha():
        word = self.get_word()
        return Token(TokenType.WORD, word)

    if self.program_str[self.pos] in '1234567890':  #added zero to this string NR
        number = self.get_number()
        return Token(TokenType.NUMBER, number)
          
        #list of operator tokens (self delimiting)
          
    if self.program_str[self.pos] == '-':
        self.pos += 1
        return Token(TokenType.SUBTRACT)

    if self.program_str[self.pos] == '+':
        self.pos += 1
        return Token(TokenType.ADD)         
          
    if self.program_str[self.pos] == '*':
        self.pos += 1
        return Token(TokenType.MULTIPLY)    

    if self.program_str[self.pos] == '/':
        self.pos += 1
        return Token(TokenType.DIVIDE)

    if self.program_str[self.pos] == '<':
        self.pos += 1
        return Token(TokenType.LESS)
          
    if self.program_str[self.pos] == '=':
        self.pos += 1
        return Token(TokenType.EQUAL)
    
    #no greater than operator?
    #if self.program_str[self.pos] == '>':
       # self.pos += 1
       # return Token(TokenType.GREATER)

    # list of punctuators (self delimiting)     
    if self.program_str[self.pos] == '{':
        while True:
            if self.program_str[self.pos] == '}':
                break
            self.pos += 1
        return Token(TokenType.LEFTBRACKET)
          
    if self.program_str[self.pos] == '}':
        self.pos += 1
        return Token(TokenType.RIGHTBRACKET)
          
    if self.program_str[self.pos] == ',':
        self.pos += 1
        return Token(TokenType.COMMA)
          
    if self.program_str[self.pos] == ';':
        self.pos += 1
        return Token(TokenType.SEMICOLON)
          
    if self.program_str[self.pos] == ':':
        self.pos += 1
        return Token(TokenType.COLON)
          
    if self.program_str[self.pos] == '.':
      tempPos = self.pos + 1
      if (tempPos) == len(self.program_str):
        self.pos += 1
        return Token(TokenType.PERIOD)
      else:
        msg = 'Invald decimal/period at position {}'.format(self.pos)
        raise LexicalError(msg)
          
    if self.program_str[self.pos] == '(':
        self.pos += 1
        return Token(TokenType.LEFTPARENT)
          
    if self.program_str[self.pos] == ')':
        self.pos += 1
        return Token(TokenType.RIGHTPARENT)

    # if no token matches, signal an error
        # Important need to make sure lexor works with scanner

    msg = 'invalid characters at position {}'.format(self.pos)
    raise LexicalError(msg)

  # --------------------------------------------------------

    def skip_whitespace(self):
        while self.pos < len(self.program_str) and \
            self.is_whitespace(self.program_str[self.pos]):
        self.pos += 1
        return
    
    def is_whitespace(self, ch):
        return ch in ' \n\t\r '
        
    def get_word(self):
        start = self.pos
        while self.pos < len(self.program_str) and \
              self.program_str[self.pos].isalpha():
        self.pos += 1
        return self.program_str[start : self.pos]
        
    def get_number(self):
        start = self.pos
        while self.pos < len(self.program_str) and \
            self.program_str[self.pos] in '0123456789':
        self.pos += 1
        return int( self.program_str[start : self.pos])