from app import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = "patient"

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    sso_provider = db.Column(db.String(50), nullable=True)
    sso_user_id = db.Column(db.String(255), unique=True, nullable=True)
    chat_history = db.Column(db.Text, nullable=True)  
    prompts = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)