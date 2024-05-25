## server_queue.py
POST /authenticate - mocks the authentication of a user (in our case all users have admin permissions)
POST /push - pushes a new job/result to a specific queue
PUT /pull - pulls a job from a specific queue and returns it to the user
GET /create_queue - returns all available queues
POST /create_queue - creates a new queue
DELETE /create_queue - deletes a queue at a specific index

## File Descriptions
server_queue.py includes the server side of this assignment
client_queue.py inclides test cases for the server_queue.py file (to run them simply run the file after starting the server)
config.json includes configs for the assignment ("time_to_persist" - time after which queues are stored in the db, "max_messages" - max number of messages per queue)
client.log logs every server response
