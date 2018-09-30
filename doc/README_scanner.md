# Compiler Group Project CS 4550
**Team Avalanche**
Ryan Holzapfel, Nicholas Rausch, Usman Wariach

## Description
Known Bugs

_No obvious bugs, but that is not to say our code is perfect._

Features Not Implemented

_None for the scanner component._

Optimizations

_None for the scanner component._

## How to Build
No compilation/building necessary for python3.

## How to Run
Executing the command `./flairs ./programs/<program name>` from the top level directory will execute the scanner and print_token programs which produce the tokens associated with the given Flair file and print them to the console. 

## Architecture and Design Decisions
The scanner and flair token list are modeled after the class examples. We modeled each punctuation character and end of file as its own token type, and use the token/value pair for integers and words. 
Currently, the scanner only identifies words, and the printer checks if they are keywords. We currently plan to implement this keyword recognition into the parser, though it could have gone into the scanner.