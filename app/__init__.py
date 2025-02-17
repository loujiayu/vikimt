from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import logging

db = SQLAlchemy()
migrate = Migrate()
logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_app():
	# Load environment variables
	load_dotenv()

	app = Flask(__name__)

	# Load configuration
	from app.config import Config
	app.config.from_object(Config)

	logging.info(app.config.get("SQLALCHEMY_DATABASE_URI"))
	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	
	from app.oauth import init_oauth
	init_oauth(app)

	# Register blueprints
	from app.google_auth import google_auth
	app.register_blueprint(google_auth, url_prefix="google")
	
	return app
