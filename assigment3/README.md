# Distributed Systems Assignment 3 - Message Queues Implementation by Samuel Kollár and Patrik Palenčár

## File Descriptions

server_queue.py includes the server side of this assignment
client_queue.py inclides test cases for the server_queue.py file (to run them simply run the file in the dedicaded terminal after starting the server)
config.json includes configs for the assignment ("time_to_persist" - time after which queues are stored in the db, "max_messages" - max number of messages per queue)
client.log logs every server response
persistent_queue_storage.db is a database for storing queue contents

## server_queue.py

POST /authenticate - mocks the authentication of a user (in our case all users have admin permissions)
POST /push - pushes a new job/result to a specific queue
PUT /pull - pulls a job from a specific queue and returns it to the user
GET /create_queue - returns all available queues
POST /create_queue - creates a new queue
DELETE /create_queue - deletes a queue at a specific index

update_db() - updates the database every x seconds (x is from the configuration file default 60 seconds) by the queue content.

Remark: We used simple list for storing different queues. We are aware that this is not the best solution for a real-world application but it is sufficient for this assignment. You can specify the queue that you want to interact with by specifying the index_nr in the json request.
## client_queue.py

We use this file as a test client, containing the client-side logic. It is responsible for making requests to the servers and handling the responses. It contains calls for each of the method of each service. We have different http requests for each of the methods. By specifying json in the call we can choose the index_nr of the queue we want to interact with. 

## Persistent Queue Storage

In server_queue.py a thread is started which saves the queues per specified time in the config.json file to a database
On startup the queues are loaded from the database. The values that we store in the database are serialized with pickle.
