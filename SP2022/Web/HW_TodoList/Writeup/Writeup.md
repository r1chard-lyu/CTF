# hw_TodoList

1. 首先來到這個網站，然後可以註冊跟登入，於是我註冊了個帳號，然後登入，但登入後看不太出來 TODO List 可以作甚麼，於是檢視一下網頁原始碼內容，可以看到按出 Report 後，會提示使用者輸入的 URL，透過 fetch 函式以 POST 方式將該 URL 以及 csrfToken 的值傳送到 '/api/report' 路徑。接下來看 hint1，Using XSS in one iframe to read another same-origin iframe，貌似這邊可以使用 XSS，於是我接下來先開始尋找這邊有哪個地方有 XSS 可以利用。

![截圖 2023-01-05 下午4.00.14.png](hw_TodoList%201c08b84bcb5f41bf81c1dc24a8e95bb5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25884.00.14.png)

![截圖 2023-01-05 下午4.03.37.png](hw_TodoList%201c08b84bcb5f41bf81c1dc24a8e95bb5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25884.03.37.png)

![截圖 2023-01-05 下午4.00.46.png](hw_TodoList%201c08b84bcb5f41bf81c1dc24a8e95bb5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25884.00.46.png)

![截圖 2023-01-05 下午4.09.02.png](hw_TodoList%201c08b84bcb5f41bf81c1dc24a8e95bb5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25884.09.02.png)

1. 看了一下網頁原始碼沒什麼想法，然後嘗試用 Burp 去擷取 /api/report 的封包看他傳送的 Request 的資訊，裡面有user 從彈跳視窗中輸入 url 及user 的 usrftoken，然後嘗試了一下要如何 XSS ，然後沒有什麼進展，這題就只要看到這邊。

![截圖 2023-01-05 下午4.20.15.png](hw_TodoList%201c08b84bcb5f41bf81c1dc24a8e95bb5/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25884.20.15.png)