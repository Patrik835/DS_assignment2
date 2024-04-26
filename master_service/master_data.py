from flask import Flask, request
from flask_restx import Resource, Api, fields
from requests import get
from datetime import datetime
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)
api = Api(app)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(Enum('submitted', 'processing', 'done', name='status_enum'), default='submitted')
    date_range = db.Column(db.String(50))
    assets = db.Column(db.String)   #array

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    assets_weights = db.Column(db.String) #array
    
    job = db.relationship('Jobs', backref='results')    

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
class Job(Resource):
    
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
            jobs = db.session.query(Jobs).filter(Jobs.status.in_(['submitted','processing', 'done'])).all() 
            return {"message": jobs}, 200

        return {"message": "Invalid credentials or permissions"}, 401

if __name__ == '__main__':
    app.run(debug=True,port=8080)