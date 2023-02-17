import requests
import random
from time import sleep

while True:
    cookies = {
        'team_token': 'c35643abd0d44913aa3a53959a244277'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = [('picked-num', random.randrange(1, 50)),('picked-num', random.randrange(1, 50)),('picked-num', random.randrange(1, 50)),('picked-num', random.randrange(1, 50)),('picked-num', random.randrange(1, 50)),('picked-num', random.randrange(1, 50))]

    r = requests.post('http://10.14.0.1/lottery/buy_lottery', cookies=cookies, data=data, headers=headers)
    print(data)
    print(r)
    sleep(0.2)