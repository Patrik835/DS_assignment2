from flask import Flask, request
from flask_restx import Resource, Api, fields
from requests import get
from master_service.app import Jobs, Results
from app import app, db

api = Api(app)

def verify_login(user, token):
    repsonse = get('http://localhost:5000/login', json={'token':token,'username':user}, headers = {'Content-Type': 'application/json'})
    if repsonse.status_code == 200:
        if repsonse.json()['token'].split(":")[1] == 'manager' or repsonse.json()['token'].split(":")[1] == 'admin':
            return True
    return False 

jobs_post_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'token': fields.String(required=True, description='Users token'),
    'date_range': fields.String(required=True, description='Date range'),
    'assets': fields.String(required=True, description='Assets'),
})

jobs_get_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of user'),
    'token': fields.String(required=True, description='Users token'),
})

@api.route('/jobs')
class Jobs(Resource):
    
    @api.expect(jobs_post_model)
    def post(self):
        args = request.json
        username = args['username']
        token = args['token']
        date_range = args['date_range']
        assets = args['assets']
        
        if verify_login(username,token):
            job = Jobs(username=username, date_range=date_range, assets=assets)
            db.session.add(job)
            db.session.commit()
            return {"message": "Job submitted"}, 200
        
        return {"message": "Invalid credentials or permissions"}, 401
    
    @api.expect(jobs_get_model)
    def get(self):
        args = request.json
        username = args['username']
        token = args['token']
        
        if verify_login(username,token):
            jobs = db.session.query(Jobs).filter(Jobs.status.in_(['processing', 'done'])).all() 
            return {"message": jobs}, 200

        return {"message": "Invalid credentials or permissions"}, 401
