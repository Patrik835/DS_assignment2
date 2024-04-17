from flask import Flask, request
from flask_restx import Resource, Api, fields
from requests import get



app = Flask(__name__)
api = Api(app)

def verify_login(user, token):
    repsonse = get('http://localhost:5000/login', json={'token':token,'username':user}, headers = {'Content-Type': 'application/json'})
    if repsonse.status_code == 200:
        return True
    return False 

jobs_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'date_range': fields.String(required=True, description='Date range'),
    'assets': fields.String(required=True, description='Assets'),
})



api.route('/jobs')
class Jobs(Resource):
    def post(self):
        args = request.json
        username = args['username']
        password = args['password']
        if verify_login(kokot,..):
            pass


if __name__ == '__main__':
    app.run(debug=True)