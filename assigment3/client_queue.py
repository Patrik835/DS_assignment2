from requests import put, get, post


headers = {'Content-Type': 'application/json'}

response = post('http://localhost:7500/queue', json={}, headers=headers)
print(response.text)
