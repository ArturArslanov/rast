from requests import get, post

req1 = get('http://127.0.0.2:8081/api/jobs')
print(req1.json())
req2 = get('http://127.0.0.2:8081/api/jobs/1')
print(req2.json())
req3 = get('http://127.0.0.2:8081/api/jobs/91239')  # пытается взять  айди которого не существует
print(req3.json())
req4 = get('http://127.0.0.2:8081/api/jobs/ert')  # пытается взять айди как строку
print(req4)

req5 = post('http://127.0.0.2:8081/api/jobs',
            json={'job': 'real_job2', 'work_size': 20, 'collaborators': '1, 2',
                  'is_finished': False, 'user_id': 1})
print(req5)
req6 = post('http://127.0.0.2:8081/api/jobs',
            json={'job': 'real_job2', 'work_size': 20, 'collaborators': '1, 2',
                  'is_finished': False, 'user_id': 1, 'id': 96})
print(req6.json())
req7 = post('http://127.0.0.2:8081/api/jobs',
            json={'job': 'real_job2', 'work_size': 20, 'collaborators': '1, 2',
                  'is_finished': False,
                  'user_id': 1, 'id': 96})  # пытается создать уже созданныйранее
print(req7)
