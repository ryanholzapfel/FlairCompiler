0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LDC 5,-1(0)  #initialize status ptr
3: LDC 6,2(0)   #initialize top ptr
4: LDA 1,6(7)  #load return address
5: ST 1,1(6)   #store return address
6: ST 5,7(6)
7: LDA 5,1(6)
8: ST 6,8(6)
9: LDA 6,9(6)
11: LD#retrieve stored value
12: LDC 2,1(0)  #literal one
13: OUT 2,0,0   #return result of main
14: HALT 0,0,0  #stop execution; end of program
