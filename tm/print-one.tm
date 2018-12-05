0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
*-------------function main
2: LDC 2,1(0) #load zero arg case
3: ST 2, 11(0) #Store zero arg case to dmem 11
5: LD 2,11(0)  # load return address from dmem in imem
6: OUT 2,0,0   #return result of main
7: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
4: LDA 7, 5(0)
