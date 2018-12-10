0: LD 2,1(0) #load program arg n to dmem
1: ST 2, 12(0) #Store cmd Line arg n case to dmem 12
*-------------function Bool
2: LDC 2,n(0) #load zero arg case
3: ST 2, 11(0) #Store zero arg case to dmem 11
4: LD 2,11(0)  # load return address from dmem in imem
5: OUT 2,0,0   #return result of main
6: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
