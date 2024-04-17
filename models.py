from master_data import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(50))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(Enum('submitted', 'processing', 'done', name='status_enum'), default='submitted')
    date_range = db.Column(db.String(50))
    assets = db.Column(ARRAY(db.Integer))

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    assets_weights = db.Column(ARRAY(db.Float))
    
    job = db.relationship('Job', backref='results')    