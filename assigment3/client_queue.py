import logging
from requests import put, get, post, delete

logging.basicConfig(filename='client.log', level=logging.INFO)


headers = {'Content-Type': 'application/json'}

#creating queue
response = post('http://localhost:7500/create_queue', json={}, headers=headers)
logging.info(f"Sent POST request to http://localhost:7500/create_queue, received status code: {response.status_code}")
print(response.text)


response = post('http://localhost:7500/push', json={"assets":"asset1"}, headers=headers)
logging.info(f"Sent POST request to http://localhost:7500/push, received status code: {response.status_code}")
print(response.text)

#printing all queues
response = get('http://localhost:7500/create_queue', json={}, headers=headers)
logging.info(f"Sent GET request to http://localhost:7500/create_queue, received status code: {response.status_code}")
print(response.text)

response = put('http://localhost:7500/pull', json={"index_nr":0}, headers=headers)
logging.info(f"Sent PUT request to http://localhost:7500/pull , received status code: {response.status_code}")
print(response.text)

response = delete('http://localhost:7500/create_queue', json={"index_nr":0}, headers=headers)
logging.info(f"Sent DELETE request to http://localhost:7500/create_queue , received status code: {response.status_code}")
print(response.text)

#printing all queues to check if queue was deleted
response = get('http://localhost:7500/create_queue', json={}, headers=headers)
logging.info(f"Sent GET request to http://localhost:7500/create_queue, received status code: {response.status_code}")
print(response.text)