import requests
from requests.exceptions import Timeout
from datetime import datetime


url="https://pyscript.ctf.zoolab.org"

f = open( 'flag_check.txt' , mode = 'r+' )
test_code = {"file" : f  }

# request
try:
    r = requests.post(url, files=test_code )
    print(r.status_code)
    print(r.text)
    t = r.elapsed
    if ( t.seconds >= 1):
        print("Yes, Response time is ", t.seconds)
    else:
        print("No, Response time is", t.seconds)

except requests.exceptions.RequestException:
    print('timeout')


