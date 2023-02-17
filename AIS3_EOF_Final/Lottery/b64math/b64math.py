#!/usr/local/bin/python3

import random
from base64 import *

a = random.randint(1, 100)
b = random.randint(1, 100)
result = a/b



def f(a, b):
    return b64decode(f'{a}/{b}'.encode()).decode()

print(f(a,b))
print(result)