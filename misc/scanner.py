from enum      import Enum
from token_agl import Token, TokenType

class State(Enum):
    looking = 1
    zero    = 2
    integer = 3
    string  = 4
    
def scan(program):
    tokens = []     # list of tokens to return
    accum  = ''     # for building multi-character tokens

    # the state machine
    state = State.looking
    pos   = 0
    while pos < len(program):
        # print(pos, ' ', state)           # trace flow
        if state == State.looking:
            if program[pos].isspace():
                pass
            elif program[pos] == ';':
                tokens.append( Token(TokenType.terminator) )
            elif program[pos] in '0':
                accum = program[pos]
                state = State.zero
            elif program[pos] in '123456789':
                accum = program[pos]
                state = State.integer
            else:
                accum = program[pos]
                state = State.string
            pos += 1
        elif state == State.zero:
            if program[pos].isspace():
                tokens.append( Token(TokenType.integer, 0) )
            elif program[pos] == ';':
                tokens.append( Token(TokenType.integer, 0) )
                tokens.append( Token(TokenType.terminator) )
            elif program[pos].isdigit():
                error_msg ='Integers do not have leading zeros: 0{}'
                raise ValueError(error_msg.format(program[pos]))
            else:
                error_msg ='Invalid character after a 0: 0{}'
                raise ValueError(error_msg.format(program[pos]))
            accum = ''
            state = State.looking
            pos  += 1
        elif state == State.integer:
            if program[pos].isdigit():
                accum += program[pos]
            elif program[pos].isspace():
                tokens.append( Token(TokenType.int_token, int(accum)) )
                accum = ''
                state = State.looking
            elif program[pos] == ';':
                tokens.append( Token(TokenType.int_token, int(accum)) )
                tokens.append( Token(TokenType.terminator) )
                accum = ''
                state = State.looking
            else:
                error_msg ='Invalid character in integer {}*{}*'
                raise ValueError(error_msg.format(accum, program[pos]))
            pos += 1
        elif state == State.string:
            if program[pos].isspace():
                tokens.append( Token(TokenType.str_token, accum) )
            elif program[pos] == ';':
                tokens.append( Token(TokenType.str_token, accum) )
                tokens.append( Token(TokenType.terminator) )
            else:
                error_msg ='All strings are single character {}*{}*'
                raise ValueError(error_msg.format(accum, program[pos]))
            accum = ''
            state = State.looking
            pos  += 1
        else:
            error_msg ='Invalid state {}.  How did that happen?'
            raise TypeError(error_msg.format(state))

    # handle accumulator at the end of the file    (I had a bug...)
    if accum:
        if state == State.zero:
            tokens.append( Token(TokenType.integer, 0) )
        elif state == State.integer:
            tokens.append( Token(TokenType.int_token, int(accum)) )
        elif state == State.string:
            tokens.append( Token(TokenType.str_token, accum) )
        else:
            error_msg ='Invalid state {} with this accum {}'
            raise TypeError(error_msg.format(state, accum))

    # return list of tokens
    return tokens

if __name__ == "__main__":
    programs = ['',          # empty program
                ' ',         # empty program with whitespace
                ';',         # one empty line
                '6 x;']      # one chunk on a line
    for p in programs:
        print( 'PROGRAM\n*{}*'.format(p) )
        print( 'SCANNED\n{}\n'.format(scan(p)) )

# ----------------------------------------------------------
# You can also read and scan program files:
#
# >>> file = open('demo.agl', 'r')
# >>> program = file.read()
# >>> print(program)
# 4 12 X;
# 8 4 b 4 X 4 b;
# 4 12 X;
# >>> print(scan(program))
# [integer = 4, integer = 12, string  = X, terminator, ...]
# ----------------------------------------------------------
