from app import db

def init_db():
    from app.models import Patient
    db.create_all()
