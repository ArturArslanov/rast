from requests import get, post

req1 = get('http://127.0.0.2:8081/api/jobs')
print(req1.json())
req2 = get('http://127.0.0.2:8081/api/jobs/1')
print(req2.json())
req3 = get('http://127.0.0.2:8081/api/jobs/91239')
print(req3.json())
req4 = get('http://127.0.0.2:8081/api/jobs/ert')
print(req4)
