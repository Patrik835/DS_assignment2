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


@api.route("/push")
class Post(Resource):
    @api.expect(post_to_queue_model)
    def post(self): #push
        if True: #user role verification ADMIN and MANAGER
            args = request.json
            all_queues[0].put(args["assets"]) #change later to specific queue
            return "Asset pushed to queue"

@api.route("/pull")
class Login(Resource):
    @api.expect()
    def put(self):
        #pull
        #user role verification ADMIN and MANAGER
        pass
    
@api.route("/create_queue")
class Login(Resource):
    def get(self):
        global all_queues
        print(all_queues)
        return_message = {}
        for index, q in enumerate(all_queues):
            print(q)
            return_message[f"Queue{index}"] = (q.queue, list(q.queue))            

    def post(self): #creating queue
        global all_queues
        if True: #user role verification ADMIN
            try:
                with open("assigment3/config.json", "r") as f:
                    max_queue_size = json.load(f)["max_messages"]
                main_queue = Queue(maxsize=max_queue_size)
                all_queues.append(main_queue)
                return "Queue created"
            except:
                return "Error creating queue"
            

    @api.expect()
    def delete(self):
        #deleting 
        #user role verification ADMIN
        pass
    
if __name__ == '__main__':
    app.run(debug=True,port=7500)