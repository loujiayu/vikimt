from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from dotenv import load_dotenv
import pyodbc
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
	# Load environment variables
	load_dotenv()

	app = Flask(__name__)

	# Load configuration
	from app.config import Config
	app.config.from_object(Config)

	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	
	from app.oauth import init_oauth
	init_oauth(app)

	# Register blueprints
	from app.google_auth import google_auth
	app.register_blueprint(google_auth)
	
	# with app.app_context():
	# 	try:
	# 		db_config = {
	# 			"server": "127.0.0.1,1433",  # Cloud SQL Proxy runs locally on port 1433
	# 			"database": "Viki_Main",
	# 			"user": "sqlserver",
	# 			"password": "3`5&^\#]))[DGt+,",
	# 			"driver": "{ODBC Driver 17 for SQL Server}"
	# 		}
	# 		conn_str = f"DRIVER={db_config['driver']};SERVER={db_config['server']};DATABASE={db_config['database']};UID={db_config['user']};PWD={db_config['password']}"
	# 		connection = pyodbc.connect(conn_str)
	# 		with connection.cursor() as cursor:
	# 			cursor.execute("SELECT GETDATE();")  # Get current date and time
	# 			result = cursor.fetchone()
	# 			print("Current Time:", result)
	# 		db.session.execute(text("SELECT 1"))
	# 		print("✅ Database connection is successful!")
	# 	except Exception as e:
	# 		print(f"❌ Database connection failed: {e}")

	return app
