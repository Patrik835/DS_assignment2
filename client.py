from requests import put, get, post

headers = {'Content-Type': 'application/json'}

response = post('http://localhost:5000/login', json={'username': 'admin', 'password':'admin'}, headers=headers)

repsonse = get('http://localhost:5000/login', json={'token':response.json()['token'],'username':'admin'}, headers=headers)

repsonse = post('http://localhost:8080/jobs', json={'token':response.json()['token'],'username':'admin','date_range':'some_range','assets':'1,2,3,4'}, headers=headers)
job_id = repsonse.json()['job_id']

repsonse = put('http://localhost:8080/jobs', json={'token':response.json()['token'],'username':'admin','assets_weights':'1:0.30,2:0.44,3:0.21,4:0.12','job_id':job_id}, headers=headers)

repsonse = get('http://localhost:8080/jobs', json={'token':response.json()['token'],'username':'admin','job_id':job_id}, headers=headers)
print(repsonse.status_code, repsonse.text)