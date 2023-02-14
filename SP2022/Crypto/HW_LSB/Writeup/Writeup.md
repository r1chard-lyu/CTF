# [HW] LSB

1. 這題目可以知道是在解 LSB，而這題的設定是有一個 Server 可以 decrypt 任意輸入的 c，並反回 c 的最後一個 bits。

![截圖 2022-10-17 下午11.25.34.png](%5BHW%5D%20LSB%2032720d4756704056a9fa5d55f8d99a74/%25E6%2588%25AA%25E5%259C%2596_2022-10-17_%25E4%25B8%258B%25E5%258D%258811.25.34.png)

1. 題目的 Server 是一個RSA解密器，然後返回 Mod 3 下的 LSB 給我們，且每次隨機生成p, q，我們 LSB Oracle Attack 去推出更高位的 bit。

1. 以下是過程
    
    
    輸入 c ( ciphertext ) 給 Server， 會返回 m%3 的值
    
    $m=a_n*3^n+a_{n-1}*3^{n-1}+...+a_1*3+a_0$
    
    ⇒ $r=a0=m\ (\ mod\ 3\ )$
    
    r 是我們接收到的數字， 然後我們再傳入 $3^{-1}*c\ (\ mod\ n)$，我們會得到 $3^{-1}*m\ (\ mod\ n)$
    
    $3^{-1}*m\ (\ mod\ n)=a_n*3^{n-1}+a_{n-1}*3^{n-2}+...+a_1+a_0*3^{-1}$
    
    ⇒ $r = a1 + (\ a0 * 3^{-1}\ (\ mod\ n)\ )\  (\ mod 3\ )$
    
    ⇒ $a1 = r - (a0 * pow(3,-1) (mod n))\ (mod 3)$
    
    $3^{-2}*c -> 3^{-2}*m$
    
    $3^{-2}*m =  an * 3^{n-2} + an-1 * 3^{n-3}+ ... + a2 + a1 * 3^{-1} + a0 * 3^{-2}$
    
    ⇒ $r = a2 + (\ a1 * 3^{-1} + a0 * 3^{-2}\ (\ mod\ n\ ))\ (\ mod\ 3)$
    
    ⇒ $a2 = r - (a1 * 3^{-1} + a0 * 3^{-2} (mod\ n))\ (mod 3)$
    
    重複上面的步驟，我們可以搜集 a0, a1, …,an 直到取到 0 ，然後我們就可以將 ( a0, a1, …,an ) 轉回bytes，就能夠得到 FLAG{lE4ST_519Nific4N7_Bu7_m0S7_1MporT4Nt}。
    

Note. 參考資料

(1) [https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack](https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack)