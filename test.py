from requests import get, post, delete

req8 = delete('http://127.0.0.2:8081/api/jobs/95')  # удалит
print(req8.json())


req1 = delete('http://127.0.0.2:8081/api/jobs/9')  # работы с таким айди не существует
print(req1.json())


req2 = get('http://127.0.0.2:8081/api/jobs/96')  # метод get
print(req2.json())
