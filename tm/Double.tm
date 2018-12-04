0: LDC 5,-1(0)  #initialize status ptr
1: LDC 6,2(0)   #initialize top ptr
2: LDA 1,6(7)  #load return address
3: ST 1,1(6)   #store return address
*-------------function Doubler
4: ST 0,1(5)   #save IMEM to DMEM
5: ST 1,2(5)   #save IMEM to DMEM
6: ST 2,3(5)   #save IMEM to DMEM
7: ST 3,4(5)   #save IMEM to DMEM
8: ST 4,5(5)   #save IMEM to DMEM
9: LDA 3,11(0) # load return adress
10: LD 4,2(0)  # load cmd line arg 1
11: LD 5,12(0)  # load cmd line arg 2 or other known variable from dmem
12: MUL 4,4,5   # multiply
13: ST 4,11(0)  # store product in DMEM at same return address handed in
14: LD 0,1(5)   #load DMEM to IMEM
15: LD 1,2(5)   #load DMEM to IMEM
16: LD 2,3(5)   #load DMEM to IMEM
17: LD 3,4(5)   #load DMEM to IMEM
18: LD 4,5(5)   #load DMEM to IMEM
20: LD 2,11(0)  # load return address from dmem in imem
21: OUT 2,0,0   #return result of main
22: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
19: LDA 7, 20(0)
