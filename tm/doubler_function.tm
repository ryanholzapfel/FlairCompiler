0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LD 2,1(0) #load program arg n to dmem
3: ST 2, 12(0) #Store cmd Line arg n case to dmem 12
*-------------function Doubler
4: LDC 2,None(0) #load zero arg case
5: ST 2, 11(0) #Store zero arg case to dmem 11
7: LD 2,11(0)  # load return address from dmem in imem
8: OUT 2,0,0   #return result of main
9: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
6: LDA 7, 7(0)
