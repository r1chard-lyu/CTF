# [HW] DH

1. 觀察題目會，發現題目會先給你一個 p，然後你要給一個 g，題目會返回 c = $(g^a)^b$ x FLAG ( Mod p )，看到 $(g^a)^b$ 可以推測這題要考的概念是 *Diffie*–*Hellman* key exchange。

1. 而我的想法是，如果我要取得 FLAG 的 long 的話，我會需要知道 c 跟 $(g^a)^b$ 的值是多少，這樣我就可以知道 FLAG =  c x  $((g^a)^b)^{-1}$ ( Mod p ) 。

1. 但是很遺憾地發現，如果給輸入一個 g ，題目只能給我 c 的結果，會沒有辦法知道 a、b 兩個隨機數分別是說少，及它們跟 g 產生的結果為何。

1. 仔細分析等式 c =  $(g^a)^b$ x FLAG ，可以確認 a、b 隨機數及 FLAG 都是不可控制的因素，我能觀察不同的只有輸入的g 及輸出的 c。

1. 那如果我今天輸入的 g=1 ，c 不就等於 $(1^a)^b$ x FLAG  = FLAG ，c = FLAG。於是我直接使用 nc連線，並輸入 1 ，題目返回 Bad :( 給我，發現題目輸入的 g 的範圍是 1 < g < p - 1，
    
    ![截圖 2022-10-17 下午9.52.14.png](%5BHW%5D%20DH%204c98f400ce8247cfa2679d5f1a44bdfd/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%25889.52.14.png)
    

1. 於是我開始想為什麼 g 的範圍要限制在 ( 1 , p -1 )，直到看完這一篇[說明](https://crypto.stackexchange.com/questions/77868/for-diffie-hellman-why-is-a-g-value-of-p−1-not-a-suitable-choice) ，解釋了為何 p-1 不適合，裡面有很明確的證明 p-1 不行的原因，這邊可以得到一個結論
    
    $( p - 1 )^k = 1\ or\ p-1$ 
    
    而我也實際使用 sagemath 證實了，如果 p =13 ，那 $( p - 1 )^k = 1\ or\ p-1$ 
    
    ```python
    #In sage 
    p = 13
    for i in range(16):
    	g = Mod(p-1,p)
    	print(g^i)
    ```
    
    ![截圖 2022-10-17 下午10.33.17.png](%5BHW%5D%20DH%204c98f400ce8247cfa2679d5f1a44bdfd/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%258810.33.17.png)
    

1. 到這邊我可以確定了，這題要找一個 g 使得 $(g^a)^b = 1$ ，這樣可以得到返回值 c = 1 x FLAG。
2. 因為知道了 $(p-1)^{2} = 1$ ，我可以假設 $t = (p-1)^{1/2}$  ，然後可以得到
    
     $t^4 = ((p-1)^{1/2})^4 = (p-1)^2 =1$ ，所以如果 $g = (p-1)^{1/2}$，他的四次方將會是 1。
    
3. 實際做了實驗也應證了這個事實，不管題目 a 跟 b 為何，我有 1/4 的機會是 $(g^a)^b =1$

![截圖 2022-10-17 下午10.31.03.png](%5BHW%5D%20DH%204c98f400ce8247cfa2679d5f1a44bdfd/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%258810.31.03.png)

1. 以下是我的過程 ( 其中試了幾次失敗，這次是成功的 )
    
    先使用 nc 連上 zoolab ，並且取得返回的 p 
    
    ![截圖 2022-10-17 下午10.43.00.png](%5BHW%5D%20DH%204c98f400ce8247cfa2679d5f1a44bdfd/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%258810.43.00.png)
    
    在 sage 輸入 p ，並取得 $g = (p-1)^{1/2}\ (\ mod p \ )$
    
    ![截圖 2022-10-17 下午10.44.55.png](%5BHW%5D%20DH%204c98f400ce8247cfa2679d5f1a44bdfd/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%258810.44.55.png)
    
    並將 g 輸入給 server ，得到了 c。
    
    ![截圖 2022-10-17 下午10.48.58.png](%5BHW%5D%20DH%204c98f400ce8247cfa2679d5f1a44bdfd/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%258810.48.58.png)
    
    使用 python，long_to_bytes 轉換 c。
    
    ```python
    #In python
    from Crypto.Util.number import long_to_bytes
    c = 38439767368662016148572678721439223408341108518077770926351753758477745847979228945453578712374003581
    print("Flag : ",long_to_bytes(c))
    ```
    
2. 最後，成功得到 Flag : b'FLAG{M4yBe_i_N33d_70_checK_7he_0rDEr_OF_G}’

Note. 參考資料

(1). [https://crypto.stackexchange.com/questions/77868/for-diffie-hellman-why-is-a-g-value-of-p−1-not-a-suitable-choice](https://crypto.stackexchange.com/questions/77868/for-diffie-hellman-why-is-a-g-value-of-p%E2%88%921-not-a-suitable-choice)