0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LDA 1,6(7)  #load return address
3: ST 1,1(6)   #store return address
4: *-------------function 1
6: OUT 2,0,0   #return result of main
7: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
5: LDA 7, 6(0)
