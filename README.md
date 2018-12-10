# Compiler Group Project CS 4550
**Team Avalanche**
Ryan Holzapfel, Nicholas Rausch, Usman Wariach

## Description
### Known Bugs
* The scanner does not check for number size (should be limited to range 2^-32 to 2^32 -1) PARTIALLY FIXED (can check positive values only, this only affects literals)
* Creating the proper semantic actions for if-then-else expressions seems to cause issues. We think the issue stems from not having semantic actions associated with primes?
* Logical operators are partially implemented, but cause various error types when tested. 
* Functions cannot call other functions or themselves
* Cannot nest operators


### Features Not Implemented
* Need a nicely formatted symbol table. Plan to use a python library that can format a dictionary into a table. 
* Code generation and three address code for If statements and Unary operators does not work/is not implemented.
* The primative operator print() is not implemented


### Features implemented by the code generator (successfully tested)
* Zero, One or Two command line arguments
* Functions only work with one or two arguments
* Less than and Equal to expressions
* All mathmatical operators


### Optimizations
_None for the scanner component._

_None for the parser component._

_None for the checker component._

_None for the generator component._

## How to Build
No compilation/building necessary for python3.

## How to Run
* All `./flair*` scripts are setup to execute only from the programs directory. If you wish to run programs from the tests directory, you need to specify the file path relative to the programs directory. (eg. `./flairc ../tests/checkAnd`)
* Executing the command `./flairs <program name>` from the top level directory will execute the scanner and print_token programs which produce the tokens associated with the given Flair file and print them to the console. 
* Executing the command `./flairf <program name>` from the top level directory executes the parser (and scanner) on the program, prints the AST tree representation if the program is successfully parsed, or prints a relevent error message if it is not.
* Executing the command `./flairv <program name>` from the top level directory executes the parser on the program and prints the symbol table.
* Executing the command `./flairc <program name>` from the top level directory executes the generator and outputs a TM program with the same name as the flair program in the tm directory


## Architecture and Design Decisions
The scanner and flair token list are modeled after the class examples. We modeled each punctuation character and end of file as its own token type, and use the token/value pair for integers and words. 
Each keyword has its own TokenType. When the scanner finds a word, it checks if that word is a keyword, and returns the apropriate token. 

The parser follows the algorithm given in class fairly closely. It uses a dictionary with NonTerminal (grammar rule) and TokenType (terminal token) tuples as keys and lists of TokenTypes and NonTerminals to expand.
The parse table was created manually by us in a spreadsheet (located in `doc`) and converted to a dictionary data structure via a script we wrote (`misc/parsetable_dict.py`)

The abstract syntax tree creation uses two components. There is a data-storage class file (semanticactions.py) where each type of AST Node has a class containing the child nodes.
In the parser, each node has a creation function that is called in the main parser class via a dictionary. The creation function looks at the semantic stack, and pops nodes as appropriate. When nodes are popped, they are stored in nodes above them in the tree. (Or in the case of integer, boolean, and identifier nodes, they contain their Token Value.)
After a program is successfully parsed, the semantic action stack contains only one node, the program node, from which the tree representation is created using class string methods. (Calling print() on the program node prints the tree.)

The semantic error symbol table uses the program node created by the AST/Parser to print a (rough) table of the program's functions, their names, inputs, and return type. Function calls are partially implemented. They won't cause the checker to error out, we currently can't accurately check types.
We can look at the symbol table for return types, but the type is not guaranteed to be there depending on the order that the functions are checked. We also added functions called/called by this function information to the symbol table.

We took two approaches to the code generator. The source file codegen.py is our first attempt (prior to lecture 24) uses a more hard-coded approach to the TM instructions, but can dynamically assign the value that the TM outputs (eg. a flair program that prints 2). 
The source file codegen2.py includes more of the TM run-time components that we have been discussing in class, but can't dynamically change the output value.
Of course, either approach would need more tree traversal functions in order to generate more complicated programs. 
We will probably expand/improve on codegen2.py going forward, but for the time being are including both files in our submission.

Three address code generation works by checking each level of the tree below a return expression node. At each level, if there is an operator, it creates a three address code with the operator it finds, and creates two new three address code identifiers for the two operators, and looks at their respective trees.
If there is no operation found, it walks the next level down the tree. When it gets to the factor level, it checks for literals and identifiers, and if one of those are found, it's value/id is passed into a new three address code. A possible optimization would be to pass the value/id back to the three address code where the operation is instead of having it in its own three address code. This is sort of handled in the code generator, where we collapse the literal/identifier three address codes back into the code containing the operator.

TM code generation is probably not as dynamic as it should be. We can successfully accomodate basic mathmatical operations and command line arguments. It iterates through each code from the three address code list, finds operators and builds TM from those operators. We have reserved DMEM addresses for each function (the main program being its own function).  DMEM 11 is always reserved for the program return value. We intended to have the ability to store all IMEM into DMEM temporarily to be able to run other functions, however, we had issues jumping between functions. So, we ended up continuously building the stack in DMEM until we were ready to return the final value. 

## Files specific to this submission
No files are specific to this submission. However, we did add some new flair tests and programs.
src/Codegen2.py was also heavily modified for this submission.
