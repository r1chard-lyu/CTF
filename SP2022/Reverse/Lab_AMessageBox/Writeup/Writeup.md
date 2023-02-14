# [Lab] AMessageBox

1. 直接用 x64dbg 開啟程式，並進入 entry point，並觀察程式行為。

![截圖 2022-11-04 下午8.24.00.png](%5BLab%5D%20AMessageBox%20a04f03bd6c044b65841577d29da950f7/%25E6%2588%25AA%25E5%259C%2596_2022-11-04_%25E4%25B8%258B%25E5%258D%25888.24.00.png)

1. 觀察輸入 flag 到 Messenge Box 彈出視窗 Wrong 這一段的組合語言程式碼，並花了一點時間理解這一段的組合語言，可以發現程式執順序會是
    
    Give me a flag → 檢查輸入字串長度 → 將輸入字串加密後，與 enc_flag 的字串一個 byte 一個 byte 比對 → 彈出 Messagebox ( Correct ! )。
    
    然後中間只要有任何一個地方檢查錯誤，就會進入 Wrong 的 branch，並彈出 Messagebox (Wrong !)
    

1. 在中間有嘗試更改程式執行的邏輯，讓程式強制進入 Correct 的 Branch ，並彈出 Messagebox( Correct ! )
    
    
    這邊更改的方式是Wrong branch 前面的 edx 更改為當時輸入的字串度大小，將 correct branch 前面的 edx 修改為 0，就可以讓程式不進入 Wrong branch ，而進去 correct brach 並彈出 correct 的 Messagebox，但這似乎無法找出 flag。
    
    ![截圖 2022-11-05 下午9.58.47.png](%5BLab%5D%20AMessageBox%20a04f03bd6c044b65841577d29da950f7/%25E6%2588%25AA%25E5%259C%2596_2022-11-05_%25E4%25B8%258B%25E5%258D%25889.58.47.png)
    
    ![截圖 2022-11-05 下午7.40.38.png](%5BLab%5D%20AMessageBox%20a04f03bd6c044b65841577d29da950f7/%25E6%2588%25AA%25E5%259C%2596_2022-11-05_%25E4%25B8%258B%25E5%258D%25887.40.38.png)
    
    ![截圖 2022-11-05 下午2.15.53.png](%5BLab%5D%20AMessageBox%20a04f03bd6c044b65841577d29da950f7/%25E6%2588%25AA%25E5%259C%2596_2022-11-05_%25E4%25B8%258B%25E5%258D%25882.15.53.png)
    
2. 從觀察的那一段組合語言中，在 第二個 loop 中找到 enc_flag 存在 eax 裡面，並一個一個將它記錄下來，就可以得到 38 個 byte 的 enc_flag。
    
    ![截圖 2022-11-05 下午10.02.56.png](%5BLab%5D%20AMessageBox%20a04f03bd6c044b65841577d29da950f7/%25E6%2588%25AA%25E5%259C%2596_2022-11-05_%25E4%25B8%258B%25E5%258D%258810.02.56.png)
    
    ```python
    enc_flag = [0xB5,0xE5,0x8D,0xBD,0x5C,0x46,0x36,0x4E,0x4E,0x1E,0xE,0x26,0xA4,0x1E,0xE,0x4E,0x46,0x6,0x16,0xAC,0xB4,0x3E,0x4E,0x16,0x94,0x3E,0x94,0x8C,0x94,0x8C,0x9C,0x4E,0xA4,0x8C,0x2E,0x46,0x8C,0x6C]
    ```
    

1. 觀察加密字串那一段組合語言，發現 輸入的字串[i] 會 先經過 rol 3 ，然後再 xor 0x87，再將byte跟 enc_flag[i] 比對，如果比對成功，就可以比對 輸入的字串[i+1]。
    
    ![截圖 2022-11-05 下午10.06.56.png](%5BLab%5D%20AMessageBox%20a04f03bd6c044b65841577d29da950f7/%25E6%2588%25AA%25E5%259C%2596_2022-11-05_%25E4%25B8%258B%25E5%258D%258810.06.56.png)
    

1. 推測出如果入的字串完全穩合，這邊就會進入 Correct Branch，於事嘗試輸入 FLAG{1111111111111111111111111111111}，FLAG開頭及38 個 byte 的字串，可以發現前面那個檢查自串比對的loop，可以成功檢查 ”FLAG{“，然後一進到 “1”，就會跳到 Wrong Branch。

1. 到這邊已經可以知道 flag → rol 3 → xor 0x87 → enc_flag ，所以，要解出 flag 只要把前面蒐集到的 enc_flag → xor 0x87 → ror 3 → flag ，就可以得到 flag ，接下來就是理解 rol 及 ror 的運算規則並實作
    
    ```python
    enc_flag = [0xB5,0xE5,0x8D,0xBD,0x5C,0x46,0x36,0x4E,0x4E,0x1E,0xE,0x26,0xA4,0x1E,0xE,0x4E,0x46,0x6,0x16,0xAC,0xB4,0x3E,0x4E,0x16,0x94,0x3E,0x94,0x8C,0x94,0x8C,0x9C,0x4E,0xA4,0x8C,0x2E,0x46,0x8C,0x6C]
    
    def ROL(data, shift, size=8):
        shift %= size 
        remains = data >> (size - shift)
        body = (data << shift) - (remains << size )
        return (body + remains)
    
    def ROR(data, shift, size=8):
        shift %= size 
        body = data >> shift
        remains = (data << (size - shift)) - (body <<size)
        return (body + remains)
    
    FLAG = ""
    for i in range(len(enc_flag)):
        FLAG+= str(chr(ROR(enc_flag[i]^0x87,3)))
    print(FLAG)
    ```
    

1. 最後，就得到 FLAG{8699314d319802ef792b7babac9da58a}

Note.

[https://blog.gye0ngje.com/353](https://blog.gye0ngje.com/353)