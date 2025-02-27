from flask import Flask, session
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
	CORS(app, supports_credentials=True)  # Allow credentials and all origins
	
	from app.resources.chathistory import ChatHistoryResource
	from app.resources.chat import ChatAPI
	from app.resources.prompt import PromptResource  # Import PromptResource
	from app.resources.patients import PatientsResource  # Import PatientsResource
	
	api = Api(app)
	api.add_resource(ChatHistoryResource, '/chathistory/<int:patient_id>')
	api.add_resource(ChatAPI, "/chat/<int:patient_id>")
	api.add_resource(PromptResource, '/prompt/<int:user_id>')  # Update PromptResource
	api.add_resource(PatientsResource, '/patients')  # Add PatientsResource

	# Load configuration
	from app.config import Config
	app.config.from_object(Config)

	app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # or 'Strict' or 'None'
	app.config['SESSION_COOKIE_SECURE'] = True
	
	if app.config.get("FLASK_ENV") == "development":
		logging.info("Running in development mode")
		# os.environ("GOOGLE_APPLICATION_CREDENTIALS") = "./viki-419417-677fe76ddb4a.json"

	logging.info(app.config.get("SQLALCHEMY_DATABASE_URI"))
	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	
	from app.oauth import init_oauth
	from app.models.patient import Patient
	from app.models.doctor import Doctor
	init_oauth(app)
	
	login_manager = LoginManager()
	login_manager.init_app(app)
	login_manager.login_view = "auth.login"

	@login_manager.user_loader
	def load_user(user_id):
			user_type = session.get("role")  # Retrieve user type from session

			if user_type == "patient":
					return Patient.query.get(int(user_id))
			elif user_type == "doctor":
					return Doctor.query.get(int(user_id))
			
			return None

	# Register blueprints
	from app.auth import auth
	app.register_blueprint(auth)
	
	return app
