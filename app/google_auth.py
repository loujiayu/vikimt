from flask import Blueprint, redirect, url_for, session, jsonify
from app import db
from app.models import Patient
from app.oauth import google
import secrets

google_auth = Blueprint("google_auth", __name__)

@google_auth.route("/")
def home():
	user = session.get("user")
	if user:
		return jsonify(user)
	return '<a href="/google/login">Login with Google2</a>'

@google_auth.route("/login")
def login():
	nonce = secrets.token_urlsafe(16)
	session["nonce"] = nonce
	return google.authorize_redirect(url_for("google_auth.authorize", _external=True), nonce=nonce)

@google_auth.route("/authorize")
def authorize():
	token = google.authorize_access_token()
	nonce = session.pop("nonce", None)

	if nonce is None:
		return "Error: Missing nonce.", 400

	user_info = google.parse_id_token(token, nonce=nonce)

	google_id = user_info.get("sub")
	email = user_info.get("email")
	name = user_info.get("name")

	user = Patient.query.filter_by(SSOUserID=google_id).first()

	if not user:
		existing_user = Patient.query.filter_by(Email=email).first()

		if existing_user:
			existing_user.SSOProvider = "Google"
			existing_user.SSOUserID = google_id
			db.session.commit()
			user = existing_user
		else:
			user = Patient(Email=email, FullName=name, SSOProvider="Google", SSOUserID=google_id)
			db.session.add(user)
			db.session.commit()

	session["user"] = {"id": user.AccountID, "name": user.FullName, "email": user.Email}
	
	return 'successful'
	# return redirect(url_for("google_auth.home"))

@google_auth.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for("google_auth.home"))
