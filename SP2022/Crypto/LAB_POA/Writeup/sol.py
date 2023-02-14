from sys import prefix
from pwn import *
import base64

r = remote('edu-ctf.zoolab.org', 10101) #nc edu-ctf.zoolab.org:10101

ct = r.readline()[:-1].decode() #ct is ciphertexr
ct = bytes.fromhex(ct) #hex to bytes
pt=b"" #pt is plaintext
assert len(ct) % 16 ==0 #ct 長度要是 16 十六的倍數
nblock = len(ct) // 16 # 向下取整數 4~5個block


for block in range(1,nblock):
    #四個 ciphertext block
    print("block ",block)
    block_pt = b''
    block_ct = ct[block * 16: (block +1) * 16] #第一個block 跟 第二個block
    last_ct = ct[(block - 1)*16: block * 16] 
    for idx in range(15, -1, -1): #15~0
        postfix = bytes([i ^ j for i, j in zip(block_pt, last_ct[idx +1:])])
        prefix = last_ct[:idx]


        for i in range(128, 256): 
            now = prefix + bytes([i ^ last_ct[idx]]) + postfix + block_ct
 
            r.sendline(now.hex().encode('ascii'))
            res = r.readline()

            if res == b"Well received :)\n":
                block_pt = bytes([i ^ 0x80]) + block_pt
                print(block_pt)
                break
        else:
            block_pt = bytes([0x80]) + block_pt

    pt += block_pt
    print(pt)



