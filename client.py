from requests import put, get, post

headers = {'Content-Type': 'application/json'}
response = post('http://localhost:5000/login', json={'username': 'admin', 'password':'admin'}, headers=headers)
print(response.status_code, response.json())

repsonse = get('http://localhost:5000/login', json={'token':response.json()['token'],'username':'admin'}, headers=headers)
print(repsonse.status_code, repsonse.json())
