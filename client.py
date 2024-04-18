from requests import put, get, post

headers = {'Content-Type': 'application/json'}

response = post('http://localhost:5000/login', json={'username': 'admin', 'password':'admin'}, headers=headers)

repsonse = get('http://localhost:5000/login', json={'token':response.json()['token'],'username':'admin'}, headers=headers)

repsonse = post('http://localhost:8080/jobs', json={'token':response.json()['token'],'username':'admin','date_range':'nigga','assets':'1,2,3,4'}, headers=headers)
print(repsonse.status_code, repsonse.text)

repsonse = get('http://localhost:8080/jobs', json={'token':response.json()['token'],'username':'admin'}, headers=headers)
print(repsonse.status_code, repsonse.text)