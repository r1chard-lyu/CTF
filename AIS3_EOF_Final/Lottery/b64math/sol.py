from pwn import *
from base64 import *

r = remote('jp.zoolab.org', 10054)

question = r.recv()
q1 = str(question).split(' / ')


print(question)
a = q1[0][-2:]
b = q1[1][:2]


def f(a, b):
    print(a)
    print(b)
    print(f'{a}/{b}')
    return b64decode(f'{a}/{b}'.encode()).decode()

f(a,b)



#r.interactive()