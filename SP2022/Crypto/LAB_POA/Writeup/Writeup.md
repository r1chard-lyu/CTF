# [LAB] POA

1.這個 Lab 是在幫助我們理解 CBC Mod 的 Padding Oracle Attack (POA)。

Padding  : 填充的意思，Encryption 時，演算法會以8或16(以上)的bytes為一區塊加密,當加密的內容不到八個bytes時，演算法會自動塞值(padding)到滿8個bytes時才做加密的動作。

Oracle : 我直接翻譯為中文成 神諭，把他當成是一個回覆，當你傳送區塊進去之後，Server 會回覆你 Padding 正確或是 Padding 錯誤，分別表示填充值正不正確。

Padding Oracle Attack：在已知 密文 及 IV( Initial vector )下，對 IV 進行修改，並透過狀態來破解中間值。而這裡的 Padding 會按照 PKCS#7 的標準去填充，填充5個 bytes 會填充5個 0x05，8個 bytes 會填充8 個 0x08。

2.有了對 Padding Oracle Attack 的暸解後，可以開始解 Lab ，這題會先解出每一個 block 的最後一個 bytes ，然後往前解，最後將解出來的每個 block 合在一起，即可獲得 FLAG。

```python
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
```

Noe.參考資料

(1) [https://dotblogs.com.tw/kevintan1983/2010/10/05/18116](https://dotblogs.com.tw/kevintan1983/2010/10/05/18116)