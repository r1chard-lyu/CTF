FLAG=""
addr = 0x4030
enc_flag = idc.get_bytes(addr, 100)
for i in range(50):
    FLAG+=str(chr(enc_flag[i]-10))
print(FLAG)