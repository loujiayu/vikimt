from app import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = "Patient"
    AccountID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    FullName = db.Column(db.String(255), nullable=True)
    SSOProvider = db.Column(db.String(50), nullable=True)
    SSOUserID = db.Column(db.String(255), unique=True, nullable=True)
    ChatHistory = db.Column(db.Text, nullable=True)  # JSON formatted chat history
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    UpdatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
