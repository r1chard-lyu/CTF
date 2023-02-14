# [HW] XOR-revenge

1.  從題目可以發現這題是在考 LFSR，因為裡面有加入 if ，所以是lfsr 的變化。

2. 計算 len(output) 可以得到406，表示 flag 長度是 336 bits ( 406 - 70 )。

3. 觀察題目後面可以發現，output 的後面 70 個 bits 是沒有跟 flag 進行 XOR 運算的，這 70 個 bits 會是 lfsr 的在運算過 336 次後的直接輸出。

4.  根據講義上的推導，可以知道只要有 2n bits 的輸出，就可以列出聯立方程式，然後用高斯消去法求解，於是我嘗試稍微列了一下，聯立方程式，發現會需要 128 bits 的輸出，才可以解 64 bits 的 state ，但目前我們只知道 70 bits ，所以這樣會解不出來。

![截圖 2022-10-09 下午9.15.29.png](%5BHW%5D%20XOR-revenge%20a43593c786d244628bc3e1bc28b0d1fd/%25E6%2588%25AA%25E5%259C%2596_2022-10-09_%25E4%25B8%258B%25E5%258D%25889.15.29.png)

$s64 = p0s0 + p1s1 + ... + p63s63\\
s65 = p0s1 + p1s2 + ... + p63s64\\
s66 = p0s2 + p1s3 + ... + p63s65\\
s67 = p0s3 + p1s4 + ... + p63s66\\
s68 = p0s4 + p1s5 + ... + p63s67\\
...\\
s128 = p0s64 + p1s65 + ... + p63s127$

5.再觀察一次題目會發現，lfsr 每運轉 37次，才會用 getbit 取得 1 個 bits，但還是想不明白，題目加了這個 if 判斷後，要怎麼去實現 Compainion matrix。

```python
if state & (1 << 64):
        state ^= 0x1da785fc480000001
```

6.然後研究了一些線性代數的定義，看了一些網路文章，直到確實讀完這篇介紹 LFSR 的 Wiki ，題目的那個 if xor ，就是在表達 **Galois LFSRs** 。而這會寫成一個 branch 的原因，是因為 only the output bit must be examined individually，這會使得 software implementation 效率更好。

[Linear-feedback shift register - Wikipedia](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)

![截圖 2022-10-16 下午11.19.16.png](%5BHW%5D%20XOR-revenge%20a43593c786d244628bc3e1bc28b0d1fd/%25E6%2588%25AA%25E5%259C%2596_2022-10-16_%25E4%25B8%258B%25E5%258D%258811.19.16.png)

![截圖 2022-10-16 下午11.11.00.png](%5BHW%5D%20XOR-revenge%20a43593c786d244628bc3e1bc28b0d1fd/%25E6%2588%25AA%25E5%259C%2596_2022-10-16_%25E4%25B8%258B%25E5%258D%258811.11.00.png)

7.而wiki的下面也分別寫了 Fibonacci 和 Galois 的 Matrix forms，這也直接為我解答了 5. 遇到的疑問，我們會需要用到 Galois 的 Matrix forms。

![截圖 2022-10-16 下午11.23.28.png](%5BHW%5D%20XOR-revenge%20a43593c786d244628bc3e1bc28b0d1fd/%25E6%2588%25AA%25E5%259C%2596_2022-10-16_%25E4%25B8%258B%25E5%258D%258811.23.28.png)

8.在學習 sagemath 的過程中，發現sagemath 裡面有一些線定代數可以用到的函式，包括 compainion matrix。查了一下，只要給一個 polynomial ，就會返回一個 Companion_matrix 矩陣，因此我用這個方式直接生成一個 Companion matrix，於是我就可以得到一個 Galios 的 Companion matrix，並且可以直接用它來計算下一個 state 的狀態，也可以用它的反矩陣計算前一個狀態，如下圖所示。

![截圖 2022-10-19 上午12.00.47.png](%5BHW%5D%20XOR-revenge%20a43593c786d244628bc3e1bc28b0d1fd/%25E6%2588%25AA%25E5%259C%2596_2022-10-19_%25E4%25B8%258A%25E5%258D%258812.00.47.png)

$Let\ \ Ｃ＝ \begin{pmatrix} c_{1}&1&0&\cdots &0\\ c_{2}&0&1&\ddots &\vdots \\
 \vdots &\vdots &\ddots &\ddots&0\\ 
c_{n-1}&0&\cdots &0&1\\ 
1&0&\cdots &0 &0 \end{pmatrix}$$,S_0=\begin{pmatrix} 
a_{1}\\ 
a_{2}\\
\vdots \\ 
a_{n-1}\\ 
a_{n}\\ \end{pmatrix}$

$Ｃ\cdot S_0＝ S_1$ 

⇒$\begin{pmatrix} 
c_{1}&1&\cdots &0&0&0\\ 
c_{2}&0&\cdots &0&0&0 \\
c_{3}&0&\cdots &0&0&0 \\
 \vdots &\vdots &\ddots &\vdots&\vdots&\vdots\\ 
c_{n-1}&0&\cdots &0&0&1\\ 
1&0&\cdots &0&0&0 \end{pmatrix}$$\begin{pmatrix} 
a_{1}\\ 
a_{2}\\
\vdots \\ 
a_{n-1}\\ 
a_{n}\\ \end{pmatrix}$= $\begin{pmatrix} 
a_{1}c_{1}+a_{2}\\ 
a_{1}c_{2}+a_{3}\\ 
\vdots \\ 
a_{1}c_{n-2}+a_{n-1}\\
a_{1}c_{n-1}+a_{n}\\ 
a_{1}\\ 
\end{pmatrix}$

$Ｃ^{-1}\cdot S_1＝ S_0$

⇒$\begin{pmatrix}
&0&0\ \ \ \cdots &0&0&1\\
&1&0\ \ \ \cdots &0&0&c1\\ 
&0&1\ \ \ \cdots &0&0&c2\\ 
&\vdots&\vdots&\vdots&\vdots&\vdots\\ 
&0&0\ \ \ \cdots &1&0&c_{n-2}\\ 
&0&0\ \ \ \cdots &0&1&c_{n-1}\\ 
\end{pmatrix}$$\begin{pmatrix} 
a_{1}c_{1}+a_{2}\\ 
a_{1}c_{2}+a_{3}\\ 
\vdots \\ 
a_{1}c_{n-2}+a_{n-1}\\
a_{1}c_{n-1}+a_{n}\\ 
a_{1}\\ 
\end{pmatrix}$= $\begin{pmatrix} 
a_{1}\\ 
a_{2}\\
\vdots \\ 
a_{n-1}\\ 
a_{n}\\ \end{pmatrix}$

9. 因為 lfsr 的輸出，getbit 會空轉 36 次，第 37 次才是輸出，所以會要再將取得的 Companion matrix ^ 37 會得到一個大的 Companion matrix ，這個 Companion matrix 才是我們要的Companion matrix。

```python
#find Companion matrix
F.<x> = PolynomialRing(GF(2))
poly = 0x1da785fc480000001
P = 0
for i in range(65):
    if (poly & 1):
        P += x^i
    poly >>= 1
c = companion_matrix(P, "left")
C = c^37
print(C)
```

1. 然後透過反矩陣的方式用秘文的最後 64 bits 計算回 initial state 的64 bits。

```python
#find initial state
M = matrix(GF(2), 64)
# C * s0 = s => s0 = M^-1 * s
s = output[-64:]
s = vector(GF(2), s)
for i in range(64):
    M[i] = (C^(i+343))[-1]
s0 = M ^ -1 * s
```

1. 有了 initial state 之後，將其跟 Companion Matrix 算出原本輸出的 406bits output，可以取得 original output ( 原本 LFSR 的輸出）。

```python
#find original output
state = s0
original_output = []
for i in range(406):
    state = C * state
    t = state[63]
    original_output.append(t)
print(original_output)
```

1. 將 original_output  跟題目的 output  做 XOR 運算並轉換後，即可取得 FLAG{Y0u_c4N_nO7_Bru73_f0RCe_tH15_TiM3!!!}

Note.參考資料

(1) [https://en.wikipedia.org/wiki/Linear-feedback_shift_register](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)

(2) [https://doc.sagemath.org/pdf/en/reference/matrices/matrices.pdf](https://doc.sagemath.org/pdf/en/reference/matrices/matrices.pdf)