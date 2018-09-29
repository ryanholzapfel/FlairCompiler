from flair_tokens import Token, TokenType
from error   import LexicalError

class Scanner:
#Read tokens from an input stream

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
  #booleans keyidentifiers and identifiers to be handled as identifiers 

  def get_next_token(self):
    self.skip_whitespace()
  
    if self.pos >= len(self.program_str):
      return Token(TokenType.EOF)  
  
    if self.program_str[self.pos].isalpha():
      identifier = self.get_identifier()
      if identifier == "if":
        return Token(TokenType.IF)
      elif identifier == "then":
        return Token(TokenType.THEN)	
      elif identifier == "else":
        return Token(TokenType.ELSE)
      elif identifier == "not":
        return Token(TokenType.NOT)
      elif identifier == "OR":
        return Token(TokenType.OR)
      elif identifier == "and":
        return Token(TokenType.AND)
      elif identifier == "print":
        return Token(TokenType.PRINT)
      elif identifier == "begin":
        return Token(TokenType.BEGIN)
      elif identifier == "end":
        return Token(TokenType.END)
      elif identifier == "return":
        return Token(TokenType.RETURN)
      elif identifier == "program":
        return Token(TokenType.program)
      elif identifier == "function":
        return Token(TokenType.FUNCTION)
      else:
        return Token(TokenType.IDENTIFIER, identifier)  
    if self.program_str[self.pos] in '1234567890':
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
      #add case to catch possible illegal decimal point NR
      #while True:
      #  if self.pos == len(self.program_str):
      #    break
      #  elif self.pos != len(self.program_str):
      #    if self.program_str[self.pos + 1].isalpha():
      #      break
      #    break
      #  elif self.program_str[self.pos + 1] in '1234567890':
      #    msg = 'invald decimal point at position {}'.format(self.pos)
      #    raise LexicalError(msg)
      self.pos += 1
      return Token(TokenType.PERIOD)
          
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
  #  --------------------------------------------------------  
  def skip_whitespace(self):
    while self.pos < len(self.program_str) and \
        self.is_whitespace(self.program_str[self.pos]):
      self.pos += 1
    return
  
  def is_whitespace(self, ch):
    return ch in ' \n\t\r '
      
  def get_identifier(self):
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
