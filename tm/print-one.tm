*-------------function main
0: LDC 2,1(0) #load zero arg case
1: ST 2, 11(0) #Store zero arg case to dmem 11
2: LD 2,11(0)  # load return address from dmem in imem
3: OUT 2,0,0   #return result of main
4: HALT 0,0,0  #stop execution; end of program
*--------- BackPatched Jumps
