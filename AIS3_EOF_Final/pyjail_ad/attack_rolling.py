import os
import requests
import json
from time import sleep
from time import time
import login

session = ''
results = {}


def decode_flag (flag_enc):
    flag_enc = flag_enc.encode()
    flag = ''
    for i in range(32):
        flag += chr(flag_enc[i] ^ 1)
    return flag

def submit_flag (flags):
    url = "http://10.6.0.1:8889/flag"
    headers = {"Content-Type": "application/json"}
    obj = {
        "flags": flags,
        "token": "c35643abd0d44913aa3a53959a244277"
    }

    r = requests.post(url, headers=headers, data=json.dumps(obj))
    data = r.json()
    return data


def send_code (teamid, code=open("code_src.py").read()):
    url = f"http://10.11.0.1:5000/api/attack/{teamid}"
    headers = {
        "Cookie": f"""session={session}""",
        "Content-Type": "application/json"
    }
    data = {"code": code}

    response = requests.post(url, headers=headers, json=data)

    try:
        obj = response.json()
        results[teamid] = obj["result"]
        flag = obj["stdout"]
        return flag
    except Exception as e:
        # print to stderr
        print(e)
        print(obj)
        return 'llll'


def helper(targets):
    targets = list(targets)
    flags = []
    for i in targets:
        if i == 22:
            continue
        print("attacking team", i, end=': ')
        flag_enc = send_code(i)
        flag = decode_flag(flag_enc)
        print(flag)
        flags.append(flag)
        
    results = submit_flag(flags)

    wrong = []
    for i, target in enumerate(targets):
        if results[i] != "Duplicated" and results[i] != "Accept" and results[i] == "Wrong":
            wrong.append(target)
        else:
            print("not possible")
            print("team", target, ":", results[i])
    print(results)
    print(wrong)
    sleep(0.3)
    return wrong

def main ():
    session = login.get_session()
    wrong = []
    wrong += helper(range(1, 7))
    wrong += helper(range(7, 12))
    wrong += helper(range(12, 18))
    wrong += helper(range(18, 25))
    print(wrong, file = open("log.txt", "w"))
    

if __name__ == '__main__':
    while True:
        main()