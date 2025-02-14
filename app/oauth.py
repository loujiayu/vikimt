from authlib.integrations.flask_client import OAuth
from flask import session
from app.config import Config

oauth = OAuth()
google = oauth.register(
    name="google",
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
    client_kwargs={"scope": "openid email profile"}
)

def init_oauth(app):
    oauth.init_app(app)
