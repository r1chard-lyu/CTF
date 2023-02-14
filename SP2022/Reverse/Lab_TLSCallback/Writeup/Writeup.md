# [Lab]TLS_Callback

1.拿到檔案後，先使用 IDA Pro 開啟程式，發現程式的流程滿清楚的，第 10 行 跟第 11 行是要求輸入一個flag 字串，然後第 16行到第25行，可以看出這段程式碼再進行加密，然後會在第25 行地方做 加密過後的 flag 的 check，因此我們可以很快的撰寫 script 去解 byte_140022B8 的 enc_flag。

![截圖 2022-11-22 下午9.24.05.png](%5BLab%5DTLS_Callback%20204c08eda791479babf948c55b7285ba/%25E6%2588%25AA%25E5%259C%2596_2022-11-22_%25E4%25B8%258B%25E5%258D%25889.24.05.png)

```python
enc_flag = [
  0x46, 0x99, 0xF7, 0x64, 0x1D, 0x79, 0x44, 0x22, 0xC1, 0xD3, 
  0x27, 0xCD, 0x31, 0xC1, 0xD9, 0x77, 0xEC, 0x7A, 0x75, 0x24, 
  0xBF, 0xDD, 0x24, 0xDD, 0x23, 0xB2, 0xCD, 0x7C, 0x02, 0x58, 
  0x46, 0x24, 0xAC, 0xD8, 0x21, 0xD1, 0x5D, 0xBC, 0xC5, 0x7C, 
  0x05, 0x6C, 0x48, 0x2B, 0xBB, 0xD5, 0x11, 0xCB, 0x35, 0xB6, 
  0xD9, 0x57, 0x0F, 0x60, 0x3F, 0x34, 0xFF, 0xEC, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00
]

key = [
  0xDE, 0xAD, 0xBE, 0xBF
]

function_list = [ 0x87, 0xff, 0x63 ]

for i in range(len(enc_flag)):
  enc_flag[i] -= key[i%4]
  enc_flag[i] ^= function_list[i%3] 
  enc_flag[i] = enc_flag[i] % 256

FLAG = "".join(map(chr,enc_flag))
print(FLAG)
```

2.但是解完會發現 flag 是錯的，於是按照這題的名稱TLS CallBack ，去思考這題是否會用到這個機制，於是在 IDA 的 Export Table 中可以看到這邊有用到 TlsCallback_1 及 TlsCallback_2，接下來去分析 這兩個 function 分別做了哪些事情，

![截圖 2022-11-22 下午9.32.33.png](%5BLab%5DTLS_Callback%20204c08eda791479babf948c55b7285ba/%25E6%2588%25AA%25E5%259C%2596_2022-11-22_%25E4%25B8%258B%25E5%258D%25889.32.33.png)

3. TlsCallback_1 中可以看到它用 function_list 去對 key 做一些運算，TlsCallback_2 會對 function_list 裡面的函數做向左位移，於是我可將這兩個寫成 python 版本的函數，從 function list 裡面的函數，點進去並研究可以判斷分別是對 0x87、0xff、0x63 做 xor 運算，因此我先用 list 將這三個數字存下來，未來取用時，會搭配 xor 去運算。

![截圖 2022-11-22 下午9.34.14.png](%5BLab%5DTLS_Callback%20204c08eda791479babf948c55b7285ba/%25E6%2588%25AA%25E5%259C%2596_2022-11-22_%25E4%25B8%258B%25E5%258D%25889.34.14.png)

![截圖 2022-11-22 下午9.36.29.png](%5BLab%5DTLS_Callback%20204c08eda791479babf948c55b7285ba/%25E6%2588%25AA%25E5%259C%2596_2022-11-22_%25E4%25B8%258B%25E5%258D%25889.36.29.png)

![截圖 2022-11-22 下午9.39.55.png](%5BLab%5DTLS_Callback%20204c08eda791479babf948c55b7285ba/%25E6%2588%25AA%25E5%259C%2596_2022-11-22_%25E4%25B8%258B%25E5%258D%25889.39.55.png)

```python
#TLSCall back 1
def TLSCall_Back1():
  for i in range(4):
    key[i] = function_list[i%3] ^ key[i]

#TLSCall back 2
function_list = [ 0x87, 0xff, 0x63 ]
def rol(list):
  temp = list[0]
  list[0] = list[1]
  list[1] = list[2]
  list[2] = temp
  return list

def TLSCall_Back2():
  rol(function_list)
```

4. 因為 TlsCallback 的函數會在程式的 main 函數之前被調用，因此，我這邊依序先呼叫 TLSCall_Back1()、TLSCall_Back2()，然後我再進行 main 函數的解碼，但發現這邊還會是錯的。

```python
TLSCall_Back1()
TLSCall_Back2()

for i in range(len(enc_flag)):
  enc_flag[i] -= key[i%4]
  enc_flag[i] ^= function_list[i%3] 
  enc_flag[i] = enc_flag[i] % 256

FLAG = "".join(map(chr,enc_flag))
print(FLAG)
```

5. 從 PE Bear 裡面可以看到這個程式會執行 TLS CallBack 的順序並不是
 TLSCall_Back1() → TLSCall_Back2()，而是TLSCall_Back2() → TLSCall_Back1() → TLSCall_Back2()，因此，我這邊只需要在 TLSCall_Back1() 前面再加入一個 TLSCall_Back2()，即可以得到 FLAG{The_first_TLS_callback_function_is_called_two_times!}

```python
TLSCall_Back2()
TLSCall_Back1()
TLSCall_Back2()

for i in range(len(enc_flag)):
  enc_flag[i] -= key[i%4]
  enc_flag[i] ^= function_list[i%3] 
  enc_flag[i] = enc_flag[i] % 256

FLAG = "".join(map(chr,enc_flag))
print(FLAG)
```