from requests import get, post, delete

req8 = delete('http://127.0.0.2:8081/api/delete_user/3')
print(req8.json())
