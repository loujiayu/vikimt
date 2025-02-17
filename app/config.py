import os

class Config:
	SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecret") 

	if os.getenv("DB_SERVER") == "127.0.0.1,1433":
		print("🔹 Using Cloud SQL Proxy for local development.") 

	# SQL Server Configuration
	DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1,1433")
	DB_NAME = os.getenv("DB_NAME")
	DB_USER = os.getenv("DB_USER")
	DB_PASSWORD = os.getenv("DB_PASSWORD") 

	SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Google OAuth
	GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
	GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
	GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
