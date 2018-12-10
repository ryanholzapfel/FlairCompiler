0: LD 2,1(0) #load program arg n to dmem
1: ST 2, 12(0) #Store cmd Line arg n case to dmem 12
*-------------function Doubler
2: LDA 3,11(0) # load return adress
3: LDC 4,2(0)  # load cmd line arg 1
4: LD 5,12(0)  # load cmd line arg 2 or other known variable from dmem
5: MUL 4,4,5   # Multiply
6: ST 4,11(0)  # store product in DMEM at same return address handed in
7: LD 2,11(0)  # load return address from dmem in imem
8: OUT 2,0,0   #return result of main
9: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
