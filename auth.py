from flask import Flask, request
from flask_restx import Resource, Api, fields

import secrets
import base64
import time

def generate_token(role):
    random_bytes = secrets.token_bytes(64)  # generate 64 random bytes
    token = base64.b64encode(random_bytes)  # encode the bytes in base64
    
    date = time.time() + 3600  # 1 hour from now
    final_token = f"{token.decode()}:{role}:{date}"
    
    return final_token # convert the bytes to a string

class UserInfo:
    def __init__(self, username, password, role="user", token=None):
        self.username = username
        self.password = password
        self.role = role
        self.token = token


app = Flask(__name__)
api = Api(app)


users_credentials = {UserInfo('admin','admin','admin')}

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'password': fields.String(required=True, description='Users password')
})
token_model = api.model('Token', {
    'token': fields.String(required=True, description='Token of user'),
    'username': fields.String(required = True, description = 'Username of user')
})

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        args = request.json
        username = args['username']
        password = args['password']
        for user in users_credentials:
            if user.username == username and user.password == password:
                user.token = generate_token(role=user.role)
                return_token = user.token.split(":")[0] + ":" + user.token.split(":")[1]
                return {"token": return_token}, 200
        return {"message": "Invalid credentials"}, 401
    
    @api.expect(token_model)
    def get(self):
        args = request.json
        token = args['token']
        username = args['username']
        for user in users_credentials:
            stored_user_token = user.token.split(":")[0] + ":" + user.token.split(":")[1]
            if token == stored_user_token and float(user.token.split(":")[2]) > time.time() and username == user.username:
                return {"message": "Valid token"}, 200
        return {"message": "Invalid token"}, 401
    
if __name__ == '__main__':
    app.run(debug=True)