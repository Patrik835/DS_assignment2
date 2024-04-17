from requests import put, get, post

headers = {'Content-Type': 'application/json'}
print(post('http://localhost:5000/login', json={'username': 'randomname', 'password':'randompassword'}, headers=headers).text)
# print(get('http://localhost:5000/pets/dog').json())