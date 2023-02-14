#! /usr/bin/python3
from Crypto.Util.number import bytes_to_long, getPrime
import random

from secret import FLAG

p = getPrime(1024)
assert bytes_to_long(FLAG) < p
print(p)

g = int(input().strip())
g %= p

if g == 1 or g == p - 1:
    print("Bad :(")
    exit(0)

a = random.randint(2, p - 2)
A = pow(g, a, p)
if A == 1 or A == p - 1:
    print("Bad :(")
    exit(0)


b = random.randint(2, p - 2)
c = pow(A, b, p) * bytes_to_long(FLAG) % p
print(c)






