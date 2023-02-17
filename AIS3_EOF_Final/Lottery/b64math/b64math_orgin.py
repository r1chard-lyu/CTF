#!/usr/local/bin/python3

import random
from base64 import b64encode

print("Welcome to the base64 math challenge!")

for rnd in range(1, 11):
    a = random.randint(1, 100)
    b = random.randint(1, 100)

    ans = input(f"{rnd}: {a} / {b} = b64encode(?) ")
    b64ans = b64encode(ans.encode('utf-8'))
    
    
    if eval(b64ans) == a / b:
        print("Correct!")
    else:
        print("Wrong!")
        exit(1)

with open('flag', 'r') as f:
    print(f.read())


# random(a,b) -> a/b, b64encode(encode(ans)) == a/b => decode(b64decode(a/b)) = ans