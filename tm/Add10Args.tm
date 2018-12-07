0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LD 2,1(0) #load program arg j to dmem
3: ST 2, 12(0) #Store cmd Line arg j case to dmem 12
4: LD 2,2(0) #load program arg i to dmem
5: ST 2, 13(0) #Store cmd Line arg i case to dmem 13
6: LD 2,3(0) #load program arg h to dmem
7: ST 2, 14(0) #Store cmd Line arg h case to dmem 14
8: LD 2,4(0) #load program arg g to dmem
9: ST 2, 15(0) #Store cmd Line arg g case to dmem 15
10: LD 2,5(0) #load program arg f to dmem
11: ST 2, 16(0) #Store cmd Line arg f case to dmem 16
12: LD 2,6(0) #load program arg e to dmem
13: ST 2, 17(0) #Store cmd Line arg e case to dmem 17
14: LD 2,7(0) #load program arg d to dmem
15: ST 2, 18(0) #Store cmd Line arg d case to dmem 18
16: LD 2,8(0) #load program arg c to dmem
17: ST 2, 19(0) #Store cmd Line arg c case to dmem 19
18: LD 2,9(0) #load program arg b to dmem
19: ST 2, 20(0) #Store cmd Line arg b case to dmem 20
20: LD 2,10(0) #load program arg a to dmem
21: ST 2, 21(0) #Store cmd Line arg a case to dmem 21
*-------------function add
22: LDA 3,11(0) # load return adress
23: LD 4,20(0)  # load cmd line arg 2 or other known variable from dmem
24: LD 5,21(0)  # load cmd line arg 2 or other known variable from dmem
25: ADD 4,4,5   # Add
26: ST 4,11(0)  # store product in DMEM at same return address handed in
27: LD 2,11(0)  # load return address from dmem in imem
28: OUT 2,0,0   #return result of main
29: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
