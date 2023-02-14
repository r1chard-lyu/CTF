ea = 0x40108b

enc_flag = idc.get_bytes(ea, 8*7)
enc_list = [enc_flag[i:i+8] for i in range(0, len(enc_flag),8)]

'''
encrypt
neg rax
xchg al,ah
'''
'''
decrypt
xchg al,ah
neg rax
'''
flag = ""
MASK = (1<<64)-1
for el in enc_list:
    #xchg al,ah
    #print(el)
    el = el[0:2][::-1] + el[2:]
    #print(el)
    el = int.from_bytes(el,'little')
    el ^= MASK
    el = (el+1)&MASK
    flag += str(int.to_bytes(el, 8, 'little').decode())
    print(int.to_bytes(el, 8, 'little').decode())
    print(flag)
#print(enc_list)








