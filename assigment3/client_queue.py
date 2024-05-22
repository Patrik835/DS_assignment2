from requests import put, get, post


headers = {'Content-Type': 'application/json'}

#creating queue
response = post('http://localhost:7500/create_queue', json={}, headers=headers)
print(response.text)

#printing all queues
response = get('http://localhost:7500/create_queue', json={}, headers=headers)
print(response.text)
