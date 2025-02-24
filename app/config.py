import os

class Config:
	SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecret") 

	if os.getenv("DB_SERVER") == "127.0.0.1":
		print("🔹 Using Cloud SQL Proxy for local development.")  

	FLASK_ENV = os.getenv("FLASK_ENV", "production")
	# SQL Server Configuration
	DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1")
	DB_NAME = os.getenv("DB_NAME")
	DB_USER = os.getenv("DB_USER")
	DB_PORT = os.getenv("DB_PORT", 5432)
	DB_PASSWORD = os.getenv("DB_PASSWORD") 
	INSTANCE_CONNECTION_NAME=os.getenv("INSTANCE_UNIX_SOCKET") 

	if FLASK_ENV == "development":
		SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
		# GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./viki-419417-677fe76ddb4a.json")
	else:
		SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"
	# SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Google OAuth
	GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
	GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
	GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
