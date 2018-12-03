0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LDA 1,6(7)  #load return address
3: ST 1,1(6)   #store return address
*-------------function main
4: LDC 2,1(0) #load zero arg case
5: ST 2, 1(0) #Store zero arg case to dmem 1
7: LDC 2,1(0) #load zero arg case
8: ST 2, 1(0) #Store zero arg case to dmem 1
9: OUT 2,0,0   #return result of main
10: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
6: LDA 7, 7(0)
