from Crypto.Util.number import long_to_bytes
from pwn import *
import gmpy

# ciphertext -> Server -> m mod 3
r = remote('edu-ctf.zoolab.org', 10102)

#先解出 x0 最低位元
#先讀出n e c
q = r.recv().split(b"\n")
n = int(q[0].decode())
e = int(q[1].decode())
c = int(q[2].decode())
inv_3 = gmpy.invert(3, int(n))
r.sendline(str(pow(inv_3,1*e,n)*c%n))
print("r :",r.recv())

inv_3 = gmpy.invert(3, n)
cnt = 0
b = 0
m = 0
i = 0

while True:
    oracle_c = (pow(inv_3, e*i, n) * c) % n
    r.sendline(str(oracle_c).encode())
    ret = int(r.recvline().decode())
    x_i = (ret - (inv_3 * b) % n) % 3
    
    if x_i == 0:
        cnt += 1
        if cnt == 10:
            break
    else:
        cnt = 0
    
    b = (inv_3 * b + x_i) % n
    m += x_i * (3 ** i)
    print(ret, x_i, i, m)
    i += 1
    print(long_to_bytes(m))
    