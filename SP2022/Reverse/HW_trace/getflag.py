FLAG=""
addr = 0x404050
text = idc.get_bytes(addr, 100)
for i in range(50):
    FLAG+=str(chr(text[i]^0x71))
print(FLAG)