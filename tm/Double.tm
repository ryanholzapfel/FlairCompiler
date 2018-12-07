0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LD 2,1(0) #load program arg n to dmem
3: ST 2, 12(0) #Store cmd Line arg n case to dmem 12
*-------------function Doubler
4: LDA 3,11(0) # load return adress
5: LDC 4,2(0)  # load cmd line arg 1
6: LD 5,12(0)  # load cmd line arg 2 or other known variable from dmem
7: MUL 4,4,5   # multiply
8: ST 4,11(0)  # store product in DMEM at same return address handed in
9: LD 2,11(0)  # load return address from dmem in imem
10: OUT 2,0,0   #return result of main
11: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
