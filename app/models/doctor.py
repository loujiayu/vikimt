from app import db
from datetime import datetime
from flask_login import UserMixin

class Doctor(UserMixin, db.Model):
	__tablename__ = 'doctor'
	
	doctor_id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	sso_provider = db.Column(db.String(100))
	sso_user_id = db.Column(db.String(255), unique=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	
	def get_id(self):
		return self.doctor_id