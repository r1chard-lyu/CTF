from pwn import *

context.arch='amd64';context.terminal=['tmux','splitw','-h']
#r = process("/chal")
r = remote("edu-ctf.zoolab.org","10008")

r.send(b"1")
r.sendlineafter(b"username\n>",b"AAAAAAAA")
r.sendlineafter(b"password\n>",b"BBBBBBBB")
gdb.attach(r)


r.interative()