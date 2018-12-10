0: LD 2,1(0) #load program arg z to dmem
1: ST 2, 12(0) #Store cmd Line arg z case to dmem 12
2: LD 2,2(0) #load program arg n to dmem
3: ST 2, 13(0) #Store cmd Line arg n case to dmem 13
*-------------function Doubler
5: LDA 3,1(0) # load return adress
6: LD 4,2(0)  # load cmd line arg 1 or other known variable from dmem
7: LD 5,12(0)  # load cmd line arg 2 or other known variable from dmem
8: MUL 4,4,5   # Multiply
9: ST 4,11(0)  # store product in DMEM at same return address handed in
10: LD 2,11(0)  # load return address from dmem in imem
11: OUT 2,0,0   #return result of main
12: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
4: LDA 7, 5(0)
