# lab_heapmath

1. 首先先用，checksec 檢查這個程式的保護機制。並且嘗試執行這個程式，可以發現程式會請求 malloc A~G 的空間，然後再依照不同的順序 Free 掉之前 malloc 的空間，而我們知道剛被釋放的 chunk 空間會被放進 bin 裡面， Tcache 會最優先被使用，而這邊我們要回答的就是 free chunk 時，在 Tcache 中每個 subbin 裡面存放chunk的連接順序（彼此會用單向的 linked list 連接)，因此我們會先需要計算每個 chunk 的大小，才會知道他們被 free 時屬於哪個 subbin，而計算 chunk 大小的方式是 :

Let malloc( 0x number ) 
⇒ Chunk Size = number (request) + 0x10 (meta data / header )- 0x2  [ 對齊 0x10 ] 

![截圖 2022-12-05 下午2.35.38.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-05_%25E4%25B8%258B%25E5%258D%25882.35.38.png)

![截圖 2022-12-05 下午2.35.56.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-05_%25E4%25B8%258B%25E5%258D%25882.35.56.png)

因此，可以寫一個函數去分類，輸入的 chunk 大小，並按照種類把它加進 list 裡面，不管答案要哪個 chunk size，只要把 list 裡面的元素轉為 A —> B —> … —> NULL ，就是這一關的答案了。

```python
list_0x20 = []
list_0x30 = []
list_0x40 = []
def classfication(char,value):
    value += 0x8
    if value <= 0x20 : 
        list_0x20.append(char)
    elif value > 0x20 and value <= 0x30 :
        list_0x30.append(char)
    elif value >= 0x30 and value :
        list_0x40.append(char)

[classfication(str(chr(str2[i][5])) ,dic[ str(chr(str2[i][5])) ]  )for i in range(14,7,-1) ]
chunk_size_0x30 = "".join([str(list_0x30[i])+" --> "  for i in range(len(list_0x30))])+"NULL"
chunk_size_0x40 = "".join([str(list_0x40[i])+" --> "  for i in range(len(list_0x40))])+"NULL"
```

1. 接下來會進入第二關，這一關會給一個上一關的數字，然後你要去計算它 chunk 跟 chunk 之間的距離，因為上一題已經寫好分類的 function ，所以這一題我只要再增加字典檔去記錄每個 chunk 的 size ，然後只要把它給的字元跟字元的距離相加就好，以下圖為例，是要算 B 跟 G 之間的距離，因此我這邊距離是 B chunk ＋C chunk ＋ Ｄchunk ＋Ｅchunk + F chunk 。
    
    ![截圖 2022-12-05 下午5.00.46.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-05_%25E4%25B8%258B%25E5%258D%25885.00.46.png)
    
    ```python
    dic_chunk_size ={}
    def classfication(char,value):
        value += 0x8
        if value <= 0x20 : 
            list_0x20.append(char)
            dic_chunk_size[char] = hex(0x20)
        elif value > 0x20 and value <= 0x30 :
            list_0x30.append(char)
            dic_chunk_size[char] = hex(0x30)
        elif value >= 0x30 and value :
            list_0x40.append(char)
            dic_chunk_size[char] = hex(0x40)
    ```
    
    ```python
    #----------- ** address chall ** -----------
    
    st3 = r.recvuntil(";")
    st4 = r.recvuntil("?")
    print(st3,st4)
    address = byte_to_hex(st3[-17:-3])
    
    start = st3[-22]
    end = st4[1]
    
    for i in range(end - start):
        print("add",chr(start))
        address += literal_eval(dic_chunk_size[chr(start)])
    
    r.sendline(hex(address).encode())
    ```
    
2. 接下來是第三關的部分，這題會給 X 跟 Y 的 malloc ，並且要求你去算它 malloc 大小，從下面這個例子為例，記憶體位置可以很清楚看到 X 跟 Y 的 chunk，X[0] 的位置是在 0x55f78ex412a0 的位址，Y[0] 是在 0x55f78ex412a0 的位址，而 unsigned long 的大小是 8 bytes，所以如果 Y[2] = “deadbeef” ，它跟 X[0] 的 index 距離是 (0x55f78ec41320 - 0x55f78ec412a0) / 8 ＝ 16。所以我們可以得到，這題的算法是，依照 malloc 的大小
[( 0x40 or 0x50 or 0x60 or 0x70 ) ＋ 0x10 ( header ) ]/ 8  的大小，就是 ? 的答案。

![截圖 2022-12-07 下午2.15.46.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25882.15.46.png)

![截圖 2022-12-07 下午2.16.58.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25882.16.58.png)

1. 第四關是延續第三關，如果將 X 跟 Y 都 Free 之後，那麽 Y chunk 的 fd 會指向何處，值得注意的是，這邊 free 後，tcache 會指向 data 而不是 header，所以這邊的距離等於一個  chunk 的大小，如果前面一題是 malloc ( 0x40 or 0x50 or x60 or x070) ，那這題 fd of Y 就是 Y 的位址減 X malloc大小 再減 Y 的 header 大小，也就是 Y - ( 0x40 or 0x50 or x60 or x070) - 0x10 。

![截圖 2022-12-07 下午2.31.52.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25882.31.52.png)

1. 第五關，這邊在考 fastbin 指向的位置，而 tcache 跟 fastbin 的 fd 最大的不同是，fastbin 的 fd 是指向 header，而 tcache 是指向 data，所以這邊的距離要在減 0x10，也就是説 fd of Y 就是 Y 的地址減  X malloc大小 再減 Y 的 header 大小再減 X header 的大小，也就是 
Y - ( 0x40/0x50/x60/x070) - 0x10 - 0x10。

![截圖 2022-12-07 下午2.50.05.png](lab_heapmath%20c4b3bca4872a4080beda9a0a5698b157/%25E6%2588%25AA%25E5%259C%2596_2022-12-07_%25E4%25B8%258B%25E5%258D%25882.50.05.png)

1. 解完這五個關卡後就可以得到FLAG{owo_212ad0bdc4777028af057616450f6654}，然後因為這題有時間限制，所以這題我有把前三關，因為要花比較多時間去算，寫成 python 的腳本去解。

```
from pwn import *
from binascii import *
from ast import literal_eval

r = remote("edu-ctf.zoolab.org","10006")

st1 = r.recvuntil("?")
str2 = st1.split(b"\n")

#----------- ** tcache chall ** -----------
def byte_to_hex(number):
    return int(number.decode("ascii"),16)

dic = { "A" : byte_to_hex(str2[1][26:30]), "B" : byte_to_hex(str2[2][26:30]), "C" : byte_to_hex(str2[3][26:30]), "D" : byte_to_hex(str2[4][26:30]), "E" : byte_to_hex(str2[5][26:30]), "F" : byte_to_hex(str2[6][26:30]), "G" : byte_to_hex(str2[7][26:30])}
dic_chunk_size ={}
list_0x20 = []
list_0x30 = []
list_0x40 = []
def classfication(char,value):
    print(char,hex(value))
    value += 0x8
    if value <= 0x20 : 
        list_0x20.append(char)
        dic_chunk_size[char] = hex(0x20)
    elif value > 0x20 and value <= 0x30 :
        list_0x30.append(char)
        dic_chunk_size[char] = hex(0x30)
    elif value >= 0x30 and value :
        list_0x40.append(char)
        dic_chunk_size[char] = hex(0x40)

[classfication(str(chr(str2[i][5])) ,dic[ str(chr(str2[i][5])) ]  )for i in range(14,7,-1) ]
print(list_0x20)
print(list_0x30)
print(list_0x40)
chunk_size_0x30 = "".join([str(list_0x30[i])+" --> "  for i in range(len(list_0x30))])+"NULL"
chunk_size_0x40 = "".join([str(list_0x40[i])+" --> "  for i in range(len(list_0x40))])+"NULL"

r.sendline(chunk_size_0x30.encode())
r.sendline(chunk_size_0x40.encode())

#----------- ** address chall ** -----------

st3 = r.recvuntil(";")
st4 = r.recvuntil("?")
address = byte_to_hex(st3[-17:-3])

start = st3[-22]
end = st4[1]

for i in range(end - start):
    address += literal_eval(dic_chunk_size[chr(start)])

r.sendline(hex(address).encode())

#---------- ** index chall ** -----------

r.interactive()
```