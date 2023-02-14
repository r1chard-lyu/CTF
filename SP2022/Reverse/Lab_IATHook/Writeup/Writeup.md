# [Lab] IATHook

1. 這題的提示是 IATHook，於是研究完跟了解 IAT Hook 的機制後，就開始去解這題，原本以為這題是要我們去竄改IAT表裡面的值( 如**[ATHook原理分析与代码编写](https://www.cnblogs.com/LyShark/p/11766620.html) )** 這篇連結裡面提到的方式，將 Correct Flag 的 MessageBox 竄改到目標 IAT 表中，讓程式去直接去呼叫 Correct 的 MessageBox，但研究了一下這支程式使用 IDA pro 的反編譯的 code，發現好像沒有這麼複雜，為什麼會這樣覺得接下來會提到。

2. 這邊使用 IDA pro 開啟程式，並在 main → main_0 找到主要的程式，並可以很明顯看出這邊程式邏輯
    
          sub_1400111A4 : 印出 “Give me flag”
       → sub_140011212 : 輸入字串 str
       → if ( j_strlen(Str) == 26) ：字串長度要是 26 才會進入 if 判斷式裡面，否則會跳出      
            MessageBoxA(”Wong”)
    
    這樣的話可以確定，輸入的字串要是 26 個 byte 的長度，然後才能進入 if 的 Branch，而這裡面也會是我們主要分析的目標。
    
    ![截圖 2022-11-10 下午11.28.07.png](%5BLab%5D%20IATHook%20032cd3a81f9b4c0081eb81b3f9e4ae98/%25E6%2588%25AA%25E5%259C%2596_2022-11-10_%25E4%25B8%258B%25E5%258D%258811.28.07.png)
    

3. 接下來分析過程是這樣，

先看 v10 但 看不出ModuleName 要幹嘛，v5 也看不出來要幹嘛，sub_1400112C6 會將 v5 跟 v10 傳入，並將 return 的值給 v9。

![截圖 2022-11-10 下午11.28.07.png](%5BLab%5D%20IATHook%20032cd3a81f9b4c0081eb81b3f9e4ae98/%25E6%2588%25AA%25E5%259C%2596_2022-11-10_%25E4%25B8%258B%25E5%258D%258811.28.07.png)

      sub_1400112C6 → sub_140011960 裡面看起來會將傳入的 v5 跟 v10 做一些像是在加密事情，然後在第25  行的地方會 return 一個看起來比較重要的指標。

![截圖 2022-11-10 下午11.29.25.png](%5BLab%5D%20IATHook%20032cd3a81f9b4c0081eb81b3f9e4ae98/%25E6%2588%25AA%25E5%259C%2596_2022-11-10_%25E4%25B8%258B%25E5%258D%258811.29.25.png)

     sub_1400111EA → sub_140011BE0 會將傳入的指標變數a1 及 整數 a2 做一些像是在加密事情，並回傳 result。

![截圖 2022-11-10 下午11.37.49.png](%5BLab%5D%20IATHook%20032cd3a81f9b4c0081eb81b3f9e4ae98/%25E6%2588%25AA%25E5%259C%2596_2022-11-10_%25E4%25B8%258B%25E5%258D%258811.37.49.png)

1. 從這邊可以推測 sub_140011960 及 sub_140011BE0 會是這題主要要分析的地方，而不是要去竄改 IAT 表的內容。而看了很久，發現 sub_1400111EA → sub_140011BE0 → sub_1400117F0，這個函數裡面看起來有比較關鍵的計算，而我也有用 x64dbg 去跑過這一段，確實可以發現這邊會做一些字串的比對，猜測這邊跟可以找到 enc_flag，及 flag 的加密運算。

![截圖 2022-11-10 下午11.53.17.png](%5BLab%5D%20IATHook%20032cd3a81f9b4c0081eb81b3f9e4ae98/%25E6%2588%25AA%25E5%259C%2596_2022-11-10_%25E4%25B8%258B%25E5%258D%258811.53.17.png)

1. 然後花了很多時間去 Trace 函數，搭配 x64dbg 去觀察函數 sub_1400117F0，可以得到byte_14001E070 是 enc_flag，a1 是 input data，a2是字串 Wrong，a3 是 26 ，a4 是一個 offset 5，最後寫一個腳本去跑這個解密的運算，就可以得到 FLAG{IAT_HoOk,MessageBoxA}。

```python
arr = bytearray.fromhex('7DD24076A714B4DC')
enc_flag = bytearray.fromhex('113E2E291C1E333B312F383D04422A32011C0F0032300016262A')
ModuleName = bytearray.fromhex('16B73218C27887EE53B62C1AA753D1A82DA02F15E670D0AE18A13376E071C09112B6351AC25CD5B219BE2537A742DDAE09A7211AF766DBA818B13476D267D1AE4EE06E12CB78B49118A13317C071F6B305934035C866C6B91EA640')
wrong = [87, 114, 111, 110, 103]

def dec(ModuleName, arr, count, offset):
    for i in range(count):
        ModuleName[i] ^= arr[i % offset]
    return ModuleName
FLAG = dec(enc_flag, wrong, 26, len(wrong))
print(FLAG)
```

Note. 

1. **[IATHook原理分析与代码编写 :** https://www.cnblogs.com/LyShark/p/11766620.html](https://www.cnblogs.com/LyShark/p/11766620.html)