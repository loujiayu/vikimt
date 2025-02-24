from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_cors import CORS
import logging
import os

db = SQLAlchemy()
migrate = Migrate()
logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(message)s "
)

def create_app():
	# Load environment variables
	load_dotenv()

	app = Flask(__name__)
	CORS(app)
	
	from app.resources.bucket import ChatHistoryResource
	from app.resources.chat import ChatAPI
	from app.resources.prompt import PromptResource  # Import PromptResource
	
	api = Api(app)
	api.add_resource(ChatHistoryResource, '/chathistory/<int:patient_id>')
	api.add_resource(ChatAPI, "/chat/<int:patient_id>")
	api.add_resource(PromptResource, '/prompt/<int:user_id>')  # Update PromptResource

	# Load configuration
	from app.config import Config
	app.config.from_object(Config)
	
	if app.config.get("FLASK_ENV") == "development":
		logging.info("Running in development mode")
		# os.environ("GOOGLE_APPLICATION_CREDENTIALS") = "./viki-419417-677fe76ddb4a.json"

	logging.info(app.config.get("SQLALCHEMY_DATABASE_URI"))
	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	
	from app.oauth import init_oauth
	from app.models.patient import Patient
	init_oauth(app)
	
	login_manager = LoginManager()
	login_manager.init_app(app)
	login_manager.login_view = "google_auth.login"
	
	@login_manager.user_loader
	def load_user(user_id):
			# Query user by ID and return user object
			return Patient.query.get(int(user_id))

	# Register blueprints
	from app.google_auth import google_auth
	app.register_blueprint(google_auth, url_prefix="/google")
	# app.register_blueprint(bucket, url_prefix="/bucket")
	
	return app
