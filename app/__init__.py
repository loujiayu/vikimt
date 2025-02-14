from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from dotenv import load_dotenv

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
	
	return app
