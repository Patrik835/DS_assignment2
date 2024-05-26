from flask import Flask, request
from flask_restx import Resource, Api, fields
import json
from queue import Queue
from requests import post
import sqlite3
import pickle
import threading
import time

app = Flask(__name__)
api = Api(app)


update_db_started = False


#on startup load all queues from db
conn = sqlite3.connect('assigment3/persistent_queue_storage.db')
c = conn.cursor()

try:
    NUM_QUEUES = c.execute('SELECT COUNT(DISTINCT queue_index) FROM queues').fetchone()[0]
except:
    NUM_QUEUES = 0

all_queues = [Queue() for _ in range(NUM_QUEUES)]

for row in c.execute('SELECT queue_index, data FROM queues ORDER BY queue_index'):
    item = pickle.loads(row[1])
    all_queues[row[0]].put(item)

conn.close()


login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'password': fields.String(required=True, description='Users password')
})
token_model = api.model('Token', {
    'token': fields.String(required=True, description='Token of user'),
    'username': fields.String(required = True, description = 'Username of user')
})

post_to_queue_model = api.model('Post', {
    'assets': fields.String(required=True, description='Assets'),
 })
set_index_model = api.model('Deqeue', {
    'assets': fields.Integer(required=True, index_nr = 0),
 })


@api.route("/authenticate")
class Auth(Resource):
    @api.expect()
    def post(self):
        return True #mocks the authentication to always reutn True as if all users where admins

@api.route("/push")
class Post(Resource):
    @api.expect(post_to_queue_model)
    def post(self): #verification ADMIN and MANAGER
        
        auth = post('http://127.0.0.1:7500/authenticate', json={}, headers={'Content-Type': 'application/json'})
        if auth: 
            args = request.json
            all_queues[0].put(args["assets"]) #change later to specific queue
            return "Asset pushed to queue"
        else:
            return "No acces rights"

@api.route("/pull")
class Dequeue(Resource):
    @api.expect(set_index_model)
    def put(self):   #verification ADMIN and MANAGER
        
        auth = post('http://127.0.0.1:7500/authenticate', json={}, headers={'Content-Type': 'application/json'})
        if auth:    
            try:
                args = request.json
                all_queues[args["index_nr"]].get()
                for index, q in enumerate(all_queues):
                    if index == args["index_nr"]:
                        return list(q.queue)     #returning queue contents to the caller
            except Exception as e:
                return f"Error pulling asset from queue {str(e)}"
        else:
            return "No acces rights"
    
@api.route("/create_queue")
class Create_delete(Resource): 
    def get(self):
        global all_queues
        return_message = {}
        for index, q in enumerate(all_queues):
            return_message[f"Queue{index}"] = list(q.queue)         
        return return_message   

    def post(self): #verification ADMIN
        global all_queues
        
        auth = post('http://127.0.0.1:7500/authenticate', json={}, headers={'Content-Type': 'application/json'})
        if auth: 
            try:
                with open("assigment3/config.json", "r") as f:
                    max_queue_size = json.load(f)["max_messages"]
                main_queue = Queue(maxsize=max_queue_size)
                all_queues.append(main_queue)
                return "Queue created"
            except:
                return "Error creating queue"
        else:
            return "No acces rights"
            

    @api.expect(set_index_model)
    def delete(self):  #verification ADMIN
        
        auth = post('http://127.0.0.1:7500/authenticate', json={}, headers={'Content-Type': 'application/json'})
        if auth:
            args = request.json
            all_queues.pop(args["index_nr"])
            return "Queue deleted"
        else:
            return "No acces rights"
    
    
#start separate thread to store queues per specified time in the db
def update_db():
    print("Starting update_db thread")
    time_to_persist = 60 #by default save the queues to db each 60 seconds
    with open("assigment3/config.json", "r") as f:
        time_to_persist = int(json.load(f)["time_to_persist"])
                    
    while True:
        try:
            conn = sqlite3.connect('assigment3/persistent_queue_storage.db')
            c = conn.cursor()

            # Delete all existing queues in the database
            c.execute('DELETE FROM queues')
            
            # Store the current state of all_queues in the database
            for queue_index, q in enumerate(all_queues):
                for item in list(q.queue):
                    # Serialize the item with pickle
                    item_data = pickle.dumps(item)
                    c.execute('INSERT INTO queues (queue_index, data) VALUES (?, ?)', (queue_index, item_data))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            
            print("Queues stored to database")

            # Wait for 60 seconds
            time.sleep(time_to_persist)
        except Exception as e:
            print(f"Error storing queues to database: {str(e)}")

if __name__ == '__main__':
    if not update_db_started:
        # Start the update_db function in a separate thread
        threading.Thread(target=update_db, daemon=True).start()
        update_db_started = True

    app.run(debug=False,port=7500)