# [HW]trojan

1. 一開始看到下載下來的檔案有兩個，一個是pcapng檔案，查了一下可以用 wireshark 打開它，有看到一些連線，但還不知道可以幹嘛。另一支是主程式，於是先直接用 IDA Pro 去靜態分析主程式。

1. 這邊花了滿多時間去研究這支程式使用 windows 函數還有圖片的函數做了哪些事情，只能大概看懂在幹嘛，很多sub_xxxxxx的函數還是沒有辦法去reverse 出他是什麼函數，以下是這支程式的分析過程 :
    
    
    a.首先找到 winMain 這個函數，裡面主要有七個函數 sub_1400017E0、sub_140001830、sub_140007C90、sub_140007D50、sub_140001560、sub140007E30、sub_14002FA0，這邊應該只要分別看懂每個函數的的功能跟運作邏輯，就可以看出這支程式做了什麼事情。
    
    ![截圖 2022-11-09 下午12.17.53.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%258812.17.53.png)
    

b.sub_1400017E0 這支函數看不太出來要幹嘛，只知道他 memset 會用 0 填滿 a1 指向的字符串的前 72 個 byte。

![截圖 2022-11-09 下午12.34.14.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%258812.34.14.png)

c. 因為用 wireshark 看過題目給 pcapng 檔案，所以可以很快知道，19832 這是 port number ，127.0.0.1 很明顯是 IP，猜測這邊 sub_140001830 及 sub 140007C90 會是跟建立網路連線有關的函數，最後將結果存在 v7。

![截圖 2022-11-09 下午12.48.05.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%258812.48.05.png)

![截圖 2022-11-09 下午12.45.22.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%258812.45.22.png)

d. sub_140007D50(v7, sub_140001560) 會將前面產生的結果 v7 做一些事情，

e. sub_140007E30(v7)，這邊看起來有 socket 函數，推測這邊是一個網路的程式( Network_function )，發現他這 socket → bind → listen ，但不知道在listen 什麼，而且這邊把 v7 放進來，很有可能是把 v7 的結果再透過這個網路函數對外傳出，並且最後會 CreatThread。

![截圖 2022-11-09 上午11.54.18.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258A%25E5%258D%258811.54.18.png)

f. 然後 sub_140002FA0 從下面這些函數來看，可以推測這是一個跟圖片有關的函數，從網路上也可以查到滿多想關的資訊的，其中比較值得注意的部分是，GetDC 是螢幕截圖的函數，sub_1400024E0 裡面的 GdipSaveImageToFile，會儲存圖片，然後其他都是在做這個圖片的一些處理，因此可以知道 sub_140002E70 這支函數，是跟圖片截圖有關的函數，

![截圖 2022-11-09 下午1.07.48.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.07.48.png)

![截圖 2022-11-09 下午1.22.21.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.22.21.png)

g. 到這邊後，開始可以去推測這支程式的邏輯，首先從名稱知道這是一支 trojan 程式，然後從 IDA pro 分析知道他會透過網路函數建立網路連線，從 wireshark 的資訊可以很明顯看到有完整的 TCP 三向交握(SYN、SYN+ACK、ACK)，這邊的話127.0.0.1:49880 是 client 端，127.0.0.1:19832 是 server端

![截圖 2022-11-09 下午1.31.09.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.31.09.png)

![截圖 2022-11-09 下午1.31.27.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.31.27.png)

然後前面有提到 sub_140007E30 不知道在 listen 什麼，到這邊後就可以理解，是這支 trojan 會在 127.0.0.1:19832 listen，實際也使用了 nc 去連線，發現確實可以建立連線，而且會有後續是可以輸入字串，從 sub_14000150→ sub140001830 這邊可以看到它要輸入的字串是 cDqr0hUUz1，但這邊輸入完之後比對一下 x64dbg 中程式執行過程，輸入的字串沒比對成功，他會直接返回，猜測這邊可能是因為 nc 的輸入會多包含”\n” 因此會比對不會成功，接下來我有想到兩個方式可以在這邊比對成功，第一個是用 python 用pwntools 去建立網路連線，直接輸入這個字串，應該就不會有 “\n” 的問題，第二個是在 x64dbg 直接更改程式的邏輯，繞過這邊，而我實際用的方式是第二個。

![截圖 2022-11-09 下午1.43.08.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.43.08.png)

![截圖 2022-11-09 下午1.45.58.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.45.58.png)

我在 15FA 這邊將 je 改成 jmp之後，再重新執行一次，結果他就返回這種亂七八糟的資料給我，猜測這個資料應該是被加密過資料。

![截圖 2022-11-09 下午1.52.47.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25881.52.47.png)

![截圖 2022-11-08 下午5.30.07.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-08_%25E4%25B8%258B%25E5%258D%25885.30.07.png)

1. 大概知道這支程式的運作過程後，可以推測，這支程式如果在我的電腦截圖並傳出，應該沒有什麼意義，想到題目有給一個pcapng ，裡面應該是這支程式產生的封包資訊，裡面有看到三個傳送比較多資料的封包，下圖中的 8、9、10 行，這裡面的資料應該是被加密過的截圖分成三個風包傳送。

![截圖 2022-11-09 下午2.22.42.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25882.22.42.png)

1. 於是我用 python 腳本將裡面的 byte 串在一起，並輸出為，發現這個檔案沒有辦法被電腦識別出來，沒有辦法被識別為什麽檔案的原因應該是因為檔案有被加密過，所以辨別不出來。

![截圖 2022-11-09 下午2.29.39.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25882.29.39.png)

1. 於是我回過頭去程式裡面找加密的函數，因為前面有用IDA pro 閱覽過一次程式，所以這邊滿快在winMain → sub_140001560 → sub_1400014B0 找到這支加密的函數，a1 是加密過後的 byte 的 data，a2 是 len(a1) ，v4 等於字串 “0vCh8RrvqkrbxN9Q7Ydx“。

![截圖 2022-11-09 下午12.03.19.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%258812.03.19.png)

把它改寫成 python code 之後會如下：

```python
a1 = data
a2 = len(a1)
for i in range(a2):
    result = a2
    if ( i >= a2 ):
      break
    a1[i] ^= list_v4[i % 0x15]
print(a1)
```

1. 將原本的 byte 的 data 使用這個 code 跑過之後，再輸出發現電腦就可以讀懂為 PNG image，將它點開後就可以得到原本的圖片及 FLAG{r3v3R53_cPp_15_pAInfUl}。

![截圖 2022-11-09 下午2.30.38.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/%25E6%2588%25AA%25E5%259C%2596_2022-11-09_%25E4%25B8%258B%25E5%258D%25882.30.38.png)

![data.png](%5BHW%5Dtrojan%205e100376dbfb4556ac5d9573ee54a087/data.png)

Note 參考資料

1. [https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectobject](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectobject)
2. [https://blog.csdn.net/kgdyouwxf/article/details/121098401?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-121098401-blog-45116301.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.1&utm_relevant_index=3](https://blog.csdn.net/kgdyouwxf/article/details/121098401?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-121098401-blog-45116301.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.1&utm_relevant_index=3)
3. Winsocket函數 : [https://learn.microsoft.com/zh-tw/windows/win32/winsock/initializing-winsock](https://learn.microsoft.com/zh-tw/windows/win32/winsock/initializing-winsock)
4. memset function : [https://www.runoob.com/cprogramming/c-function-memset.html](https://www.runoob.com/cprogramming/c-function-memset.html)
5. Socket 網路連線過程 : [http://zake7749.github.io/2015/03/17/SocketProgramming/](http://zake7749.github.io/2015/03/17/SocketProgramming/)
6. CreatThread : [https://blog.csdn.net/u012877472/article/details/49721653](https://blog.csdn.net/u012877472/article/details/49721653)
7. TCP 三向交握 ：[https://notfalse.net/7/three-way-handshake](https://notfalse.net/7/three-way-handshake)