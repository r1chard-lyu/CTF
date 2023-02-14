import base64

with open("chal_test","rb") as f :
    data = f.read()

out = base64.b64decode(data)
with open("chal_flag2","wb") as f:
    f.write(out)