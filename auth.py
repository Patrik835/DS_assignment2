from flask import Flask, request
from flask_restx import Resource, Api, fields

import secrets
import base64

def generate_token():
    random_bytes = secrets.token_bytes(64)  # generate 64 random bytes
    token = base64.b64encode(random_bytes)  # encode the bytes in base64
    return token.decode()  # convert the bytes to a string


app = Flask(__name__)
api = Api(app)

tokens = {}
users_credentials = {'randomname':"randompassword"} #username:password

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'password': fields.String(required=True, description='Users password')
})

@api.route("/login")
@api.doc(params={'username': 'Username of user', 'password': 'Users password'})
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        args = request.json
        username = args['username']
        password = args['password']
        if username in users_credentials:
            if users_credentials[username] == password:
                generate_token()
                return "success"
        else:
            return "not in dict"

if __name__ == '__main__':
    app.run(debug=True)
