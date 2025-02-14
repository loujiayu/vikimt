from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
# OAuth Configuration
oauth = OAuth(app)
app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID", google_client_id)
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET", google_client_secret)
app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"

google = oauth.register(
		name='google',
		client_id=app.config['GOOGLE_CLIENT_ID'],
		client_secret=app.config['GOOGLE_CLIENT_SECRET'],
		server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
		client_kwargs={'scope': 'openid email profile'}
)

if __name__ == '__main__':
		app.run(debug=True)
