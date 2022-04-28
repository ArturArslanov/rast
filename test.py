from requests import get, post, delete, put

# удаление
# req8 = delete('http://127.0.0.2:8081/api/jobs/95')  # удалит
# print(req8.json())
#
# req1 = delete('http://127.0.0.2:8081/api/jobs/9')  # работы с таким айди не существует
# print(req1.json())
#
# req2 = get('http://127.0.0.2:8081/api/jobs/96')  # метод get
# print(req2.json())

# изменение
req3 = get('http://127.0.0.2:8081/api/jobs')
print(req3.json())
req = put('http://127.0.0.2:8081/api/jobs/2', json={'team_leader': 1, 'work_size': 12})
print(req.json())
req4 = get('http://127.0.0.2:8081/api/jobs/2',
           json={'team_leader': 3, 'work_size': 20})  # не  правильный метод
print(req4.json())
req33 = put('http://127.0.0.2:8081/api/jobs/190000000000', json={'team_leader': 3, 'work_size':
    20})  # не существующий айди
print(req33.json())
req7 = get('http://127.0.0.2:8081/api/jobs')
print(req7.json())
