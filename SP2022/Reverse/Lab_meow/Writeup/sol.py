import ctypes

enc_flag = [36,29,27,49,33,11,79,15,-24,80,55,91,8,64,74,8,29,17,74,-72,17,103,63,103,56,20,63,25,11,84,-76,9,99,18,104,42,69,83,14]
byte_403010 = [98, 87, 86, 118, 100, 119, 61, 61, 135, 99, 0, 0, 0, 0, 0]
flag = enc_flag
for i in range(len(enc_flag)):
    flag[i] = enc_flag[i]-2*(i%3)
    flag[i] = ctypes.c_uint8(flag[i]).value
    flag[i] ^= ctypes.c_uint8(byte_403010[i % 0xB]).value

FLAG = "".join(map(chr, flag))
print(FLAG)
