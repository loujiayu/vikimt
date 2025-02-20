from app import db

def init_db():
    from app.models.patient import Patient
    db.create_all()
