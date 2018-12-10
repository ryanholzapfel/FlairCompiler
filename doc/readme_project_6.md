# Compiler Group Project CS 4550
**Team Avalanche**
Ryan Holzapfel, Nicholas Rausch, Usman Wariach

## Description
### Known Bugs
* The scanner does not look for underscores in identifiers (an underscore would cause an invalid character error)
* When a number is followed by letters, the scanner returns a number token followed by an identifier token (it should return an invalid number error)
* The scanner does not check for number size (should be limited to range 2^-32 to 2^32 -1) PARTIALLY FIXED (can check positive values only)
* Creating the proper semantic actions for if-then-else expressions seems to cause issues. We think the issue stems from not having semantic actions associated with primes?
* The code generator in the previous version works on print one only in the current version we got doubler to generate some tm code but the tm code is not operable 
* The current version has now also broken print-one tm code this was expected as the design to handle Doubler is somewhat different we expect to fix this in the near future

### Features Not Implemented
* The error handler does not filter Python errors out. It just passes everything through. (IN PROGRESS)
* Need a nicely formatted symbol table. Plan to use a python library that can format a dictionary into a table. 
* Three address code is not able to handle function calls and complex expressions. 

### Optimizations
_None for the scanner component._

_None for the parser component._

_None for the checker component._

_None for the generator component._

## How to Build
No compilation/building necessary for python3.

## How to Run
* Executing the command `./flairs ./programs/<program name>` from the top level directory will execute the scanner and print_token programs which produce the tokens associated with the given Flair file and print them to the console. 
* Executing the command `./flairf ./programs/<program name>` from the top level directory executes the parser (and scanner) on the program, prints the AST tree representation if the program is successfully parsed, or prints a relevent error message if it is not.
* Executing the command `./flairv ./programs/<program name>` from the top level directory executes the parser on the program and prints the symbol table.
* Executing the command `./flairc ./programs/<program name>` from the top level directory executes the generator and outputs a TM program with the same name as the flair program in the programs directory
* Exicuting the command `./flairc <program name>` ex: `./flairc Doubler` from the top level directory will now work --exception for existing_programs run `./flairc existing_programs/<program name>`

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
If there is no operation found, it walks the next level down the tree. When it gets to the factor level, it checks for literals and identifiers, and if one of those are found, it's value/id is passed into a new three address code. A possible optimization would be to pass the value/id back to the three address code where the operation is instead of having it in its own three address code. 
Currently, we are unable to process function calls or complex expressions (factors that resolve to expressions).

Currently broken tm code is generated for Doubler.flr we still see this as progress as now our code generator is morphing from a hard coded version to a more automated compiler that will be able to handle more than just one program

## Files specific to this submission
Project 6
* src/threeACgen.py
* src/codegen2.py (heavily modified/added to for this submission)
* src/ac_run.py (a utility to test our 3 address code, takes in a flair program, prints out the 3 address code)
* programs/threeacmultest.flr (simple flair program to test tree traversal/3 address code generation; it's not very complicated, but it's what we can parse/generate)
