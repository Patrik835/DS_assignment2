import logging
from requests import put, get, post, delete

logging.basicConfig(filename='assigment3/client.log', level=logging.INFO)

headers = {'Content-Type': 'application/json'}

#creating queue
response = post('http://localhost:7500/create_queue', json={}, headers=headers)
logging.info(f"Sent POST request to http://localhost:7500/create_queue, received status code: {response.status_code}")
print(response.text)


response = post('http://localhost:7500/push', json={"assets":"asset1","index_nr":0}, headers=headers)
logging.info(f"Sent POST request to http://localhost:7500/push, received status code: {response.status_code}")
print(response.text)

#printing all queues
response = get('http://localhost:7500/create_queue', json={}, headers=headers)
logging.info(f"Sent GET request to http://localhost:7500/create_queue, received status code: {response.status_code}")
print(response.text)

response = put('http://localhost:7500/pull', json={"index_nr":1}, headers=headers)
logging.info(f"Sent PUT request to http://localhost:7500/pull , received status code: {response.status_code}")
print(response.text)

response = delete('http://localhost:7500/create_queue', json={"index_nr":2}, headers=headers)
logging.info(f"Sent DELETE request to http://localhost:7500/create_queue , received status code: {response.status_code}")
print(response.text)


#printing all queues to check if queue was deleted
response = get('http://localhost:7500/create_queue', json={}, headers=headers)
logging.info(f"Sent GET request to http://localhost:7500/create_queue, received status code: {response.status_code}")
print(response.text)


# import sqlite3

# # Connect to the SQLite database
# # If the database does not exist, it will be created
# conn = sqlite3.connect('assigment3/persistent_queue_storage.db')

# # Create a cursor object
# c = conn.cursor()

# # Create a table to store the queues
# # Create a table to store the queues
# c.execute('''
#     CREATE TABLE IF NOT EXISTS queues (
#         id INTEGER PRIMARY KEY,
#         queue_index INTEGER NOT NULL,
#         data BLOB NOT NULL
#     )
# ''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()