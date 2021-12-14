a = ['000', '001', '010', '011', '100', '101', '110', '111']
a1 = ['00', '01', '10']

dc = {}

# for i in a1:
#     for ii in a:
#         dc.update({(i ,ii): input(str(i) + ' ' +str(ii)+ ' ')})


a = """00 000 ADDI4SPN
00 001 FLD
00 010 LW
00 011 FLW
00 100 Reserved
00 101 FSD
00 110 SW
00 111 FSW
01 000 ADDI
01 001 JAL
01 010 LI
01 011 LUI/ADDI16SP
01 100 MISC-ALU
01 101 J
01 110 BEQZ
01 111 BNEZ
10 000 SLLI
10 001 FLDSP
10 010 LWSP
10 011 FLWSP
10 100 J[AL]R/MV/ADD
10 101 FSDSP
10 110 SWSP
10 111 FSWSP"""

dc = {}
for i in a.split('\n'):
    # print(i.split(' '))
    a1,a2,a3 = i.split(' ')
    dc.update({(a1,a2): a3})
print(dc)