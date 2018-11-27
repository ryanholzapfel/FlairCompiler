# Compiler Group Project CS 4550
**Team Avalanche**
Ryan Holzapfel, Nicholas Rausch, Usman Wariach

## Description
### Known Bugs
* The scanner does not look for underscores in identifiers (an underscore would cause an invalid character error)
* When an identifier is letters followed by a number, the scanner returns an identifer token followed by a number token (it should be one identifier token)
* When a number is followed by letters, the scanner returns a number token followed by an identifier token (it should return an invalid number error)
* The parser has issues with return statements that call functions that contain multiple formals.
* The abstract syntax tree building functions that look for optional parts of the AST need to check types before building on lower nodes.
* The scanner does not check for number size (should be limited to range 2^-32 to 2^32 -1) PARTIALLY FIXED (can check positive values only)
* ~~The scanner does not check for identifier length (should be limited to 256 characters)~~ Fixed
* ~~The scanner reads numbers separated with periods as individual tokens (should return an invalid character error)~~ This is no longer considered an error?
* ~~The parser errors out on trying to expand the NonTerminal FORMALS. This seems to be an issue with our parse table.~~ Fixed


### Features Not Implemented
* The scanner still uses the function next_token() instead of next()
* The error handler does not filter Python errors out. It just passes everything through. 
* The AST is not able to be printed in a human readable format. 

### Optimizations
_None for the scanner component._
_None for the parser component._

## How to Build
No compilation/building necessary for python3.

## How to Run
Executing the command `./flairs ./programs/<program name>` from the top level directory will execute the scanner and print_token programs which produce the tokens associated with the given Flair file and print them to the console. 
Executing the command `./flairf ./programs/<program name>` from the top level directory executes the parser (and scanner) on the program, prints "Program is valid." if the program is successfully parsed, or prints a relevent error message if it is not.
Our five broken programs are in the directory `./tests/parser_fail_tests`. Point `./flairf` to a program in that directory to test those.

## Architecture and Design Decisions
The scanner and flair token list are modeled after the class examples. We modeled each punctuation character and end of file as its own token type, and use the token/value pair for integers and words. 
Each keyword has its own TokenType. When the scanner finds a word, it checks if that word is a keyword, and returns the apropriate token. 
The parser follows the algorithm given in class fairly closely. It uses a dictionary with NonTerminal (grammar rule) and TokenType (terminal token) tuples as keys and lists of TokenTypes and NonTerminals to expand.
The parse table was created manually by us in a spreadsheet (located in `doc`) and converted to a dictionary data structure via a script we wrote (`misc/parsetable_dict.py`)
The abstract syntax tree creation uses two components. There is a data-storage class file (semanticactions.py) where each type of AST Node has a class containing the child nodes.
In the parser, each node has a creation function that is called in the main parser class. The creation function looks at the semantic stack, and pops nodes as appropriate. 