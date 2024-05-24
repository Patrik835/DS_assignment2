from flask import Flask, request
from flask_restx import Resource, Api, fields
import json
from queue import Queue

app = Flask(__name__)
api = Api(app)


login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'password': fields.String(required=True, description='Users password')
})
token_model = api.model('Token', {
    'token': fields.String(required=True, description='Token of user'),
    'username': fields.String(required = True, description = 'Username of user')
})

all_queues = []
post_to_queue_model = api.model('Post', {
    'assets': fields.String(required=True, description='Assets'),
 })
set_index_model = api.model('Deqeue', {
    'assets': fields.Integer(required=True, index_nr = 0),
 })


@api.route("/push")
class Post(Resource):
    @api.expect(post_to_queue_model)
    def post(self): #push DONE done just add verification ADMIN and MANAGER
        if True: 
            args = request.json
            all_queues[0].put(args["assets"]) #change later to specific queue
            return "Asset pushed to queue"
        else:
            return "No acces rights"

@api.route("/pull")
class Dequeue(Resource):
    @api.expect(set_index_model)
    def put(self):   #pull DONE just add verification ADMIN and MANAGER
        if True:     
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
class Create_delete(Resource):      #DONE
    def get(self):
        global all_queues
        print(all_queues)
        return_message = {}
        for index, q in enumerate(all_queues):
            print(q)
            return_message[f"Queue{index}"] = list(q.queue)         
        return return_message   

    def post(self): #creating queue DONE just add verification ADMIN
        global all_queues
        if True: 
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
    def delete(self):  #deleting  DONE queue add verification ADMIN
        if True:
            args = request.json
            all_queues.pop(args["index_nr"])
            return "Queue deleted"
        else:
            return "No acces rights"
    
if __name__ == '__main__':
    app.run(debug=True,port=7500)