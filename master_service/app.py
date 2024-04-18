from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)


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

if __name__ == '__main__':
    app.run(debug=True,port=8080)