# [LAB] COR

1. 花了一點時間理解 Correlation Attack 的 75 % 相似是甚麼意思，知道了是這邊的 LFSR 叫做 Geffe Generator，假設 lfsr1 的輸出是 x1、lfsr2的輸出是 x2，lfsr3 的輸出是 x3， 並按照 x2 if x1 else x3 的規則輸出 LFSR 的 output，而老師上課有教，按照這個輸出會有一個規則，x2 的 output  跟 x3 的 output 都會跟 LFSR 的 output 有 75% 相似。因此，可以利用這個缺陷，使得原本 $2^{96}$ 的三個 lfsr 密鑰，變成 $3*2^{32}$，就可以在有限的時間內去爆破。

1. 換成這一題，觀察題目，發現 lfsr1 的 state 是 27 bits、lfsr2 的 state 是 23 bits，lfsr3 的 state 是 25 bits，如果我們直接枚舉，會有 $2^{27 + 23 + 25} = 2^{75}$   bits 要去嘗試，但如果我們使用 Correlation Attack，就可以枚舉 $2^{27}+2^{23}+2^{25}$ 次。

1. 知道上面的內容後，就可以開始去解這一題，因為這題最後沒有解出來，所以，下面附上我的解題思路 : 
    
    
    觀察題目，可以發現題目有多輸出 200 bits，這200 bits 是沒有跟 flag 做 XOR 運算，是LFSR 的直接輸出，因此我可以用這 200bits 的輸出 (output ) 跟 lfsr2 的輸出 (x2) 去比較，先枚舉 lfsr2 的state 並產生 200 個 lfs2 的輸出，這個 lfsr2 的 200 bits 輸出，只要跟 Output 的輸出有75 % 相似，就表示中了。
    
    在枚舉 lfsr3 時，也是同樣的方式，先枚舉 lfsr3 的state 並產生 200 個 lfs3 的輸出，這個 lfsr3 的 200 bits 輸出，只要跟 Output 的輸出有75 % 相似，就表示中了。
    
    然後，有了正確的 lfsr2 的 state 跟 lfsr2_output，還有 lfsr3 的 state 跟 lfsr3_output，跟 LFSR 的 Output，我們可以枚舉 lfsr1 的 state 去產生 lfsr1_output ，並利用 Output = x2 if x1 else x3 的規則，去產生輸出，這邊的輸出要跟題目的 Output 的後200bits 完全相同，則代表 lfsr1 的 state 中了。
    
    有了三個 lfsr1、lfsr2 及 lfsr3 的 state，我們就可以返推回三個 lfsr 的 initial state，然後就可以利用這三個 lfsr 的 initial state 產生輸出，再用這原始輸出跟 題目給的 output 做XOR，就可以拿到 FLAG。