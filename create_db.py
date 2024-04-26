from master_service.master_data import db, app

with app.app_context():
    db.create_all()