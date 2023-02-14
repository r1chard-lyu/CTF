import requests
from requests.exceptions import Timeout
from datetime import datetime

url1="http://localhost:8000/"
url2="https://pyscript.ctf.zoolab.org"
#


f = open( 'test.txt' , mode = 'r+' )
test_code = {"file" : f  }

# request
try:
    r = requests.post(url2, files=test_code )
    print(r.status_code)
    print(r.text)
    t = r.elapsed
    if ( t.seconds >= 1):
        print("Yes, Response time is ", t.seconds)
    else:
        print("No, Response time is", t.seconds)

except requests.exceptions.RequestException:
    print('timeout')


