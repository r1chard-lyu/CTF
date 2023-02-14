from Crypto.Util.number import getPrime, isPrime
import sys

for i in range(50,100):
    for j in range(50,100):
        for k in range(50,100):
            for l in range(50,100):
                for m in range(50,100):
                    n = (13**m)*(11**l)*(7**k)*(3**j)*(2**i)
                    if n.bit_length() == 1024:
                        if isPrime(n+1) == True :
                            p = n+1
                            print("prime is :",p)
                            sys.exit()