# [HW]AES

## **AES**

1. 這題解題的 Hint 是使用到 CPA ( Correlation Power Analysis )，但是要選擇攻擊的點，可以對AES 第一 round 做 CPA 或是最後一 round 做 CPA，使用 DPA 可能也可以直接解出這一題，Key 就是 FLAG ，解出 Key 就是解出 FLAG。
2. 而我這邊會選擇 ****SubBytes**** 做 CPA，因為這樣使用的 intermediate 函數感覺可以比在 ****ShiftRows**** 做 ********CPA 簡易。****SubBytes**** 只要直接使用 $Sbox (p⊕k)$		
		 即可，而 ShiftRows 會要用到
    
     ( $Sbox^{-1} ( ShiftRow ( c⊕k’ )$ 。
    
3. 題目有個 json 檔，在這邊 ct 是 cipher text，pt 是 plain text，及加密產生的 power comsumption 。
4. 於是可以開始去實作出這一題 CPA，方法參考老師上課的投影片。

Step 1. Choosing an intermediate value and Calculating hypothetical intermediate values 

⇒ 我這邊選擇 ****SubBytes**** 這一 Round ，並計算所有 255 種可能的 intermediate values ( **f(p,k) = Sbox** ) 。

```python
intermediate_value = []
for p in plain:
	intermediate_value.append([sbox[p ^ k] for k in range(256)])
```

Step 2.  Measure the power traces

⇒ 這邊直接取用題目給的資訊 [”pm”]

```python
power_trace = []
for p in info:
	power_trace.append(p["pm"][:250])
```

Step 3.  Choose a power model

⇒ 使用 hamming weight 來計算，並得到一個 Hamming waight  matrix。

```python
for i in range(plain.shape[0]):
	row = []
	for j in range(0, 256):
		row.append(bin(intermediate[i][j]).count("1"))
	hw.append(row)
```

Step 4. Calculate the hypothetical intermediate value and corresponding hypothetical power consumption

⇒ 

這邊計算方式是，

先將算將 Hamming waight  matrix ( D x K ) 的第一個 Column 跟 Traces Matrix ( D x T ) 的 第一個 Column 做 Correlation 。

然後將 Hamming waight  matrix ( D x K ) 的第一個 Column 跟 Traces Matrix ( D x T ) 的 第二個 Column 做 Correlation 。

…

到最後，會將 Hamming waight  matrix ( D x K ) 的第  K 個 Column 跟 Traces Matrix ( D x T ) 的 第 T 個 Column 做 Correlation 。

因此，會得到一個 K x T 的 Correlation coefficients matrix  ( 0 ≤ K ≤ 255  255 種可能) ，

Step 5. Apply the statistic analysis between measured power consumption and hypothetical power consumption ( find max in all correlation )

⇒ 到這邊就可以將得到 Correlation coefficients matrix 取得其最大的，就會是 Key 的第一個 byte。然後就可以，byte by byte 的爆出 key，即可取得 FLAG{18MbH9oEnbXHyHTR}

參考資料 

(1). [https://learningsky.io/using-python-to-encrypt-decrypt-aes-128-ecb/](https://learningsky.io/using-python-to-encrypt-decrypt-aes-128-ecb/)