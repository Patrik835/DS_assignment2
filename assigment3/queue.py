from flask import Flask, request
from flask_restx import Resource, Api, fields
from queue import Queue
import json

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

@api.route("/push")
class Login(Resource):
    @api.expect()
    def post(self):
        #push
        #user role verification ADMIN and MANAGER
        pass
    
@api.route("/pull")
class Login(Resource):
    @api.expect()
    def put(self):
        #pull
        #user role verification ADMIN and MANAGER
        pass
    
@api.route("/queue")
class Login(Resource):
    def get(self):
        return_message = {}
        for index,q in enumerate(all_queues):
            print(q)
            return_message[f"Queue{index}"] = (q.queue, list(q.queue))
        return json.dumps(return_message)
            

    def post(self): #creating queue
        if True: #user role verification ADMIN
            max_queue_size = json.loads(request.data)['max_messages']
            main_queue = Queue(maxsize=max_queue_size) 
            all_queues.append(main_queue)

    @api.expect()
    def delete(self):
        #deleting 
        #user role verification ADMIN
        pass
    
if __name__ == '__main__':
    app.run(debug=True,port=7500)