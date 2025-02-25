from flask import Blueprint, redirect, url_for, session, jsonify
from app import db
from app.models.patient import Patient
from app.models.doctor import Doctor
from flask_login import login_user, logout_user, login_required, current_user
from app.oauth import google
import secrets

auth = Blueprint("auth", __name__)

@auth.route("/")
def home():
	# user = Patient.query.filter_by(sso_user_id="773").first()
	user = current_user.get_id()
	if user:
		return jsonify(user)
	return '<a href="/login/google/patient">Login as Patient with Google</a> | ' \
           '<a href="/login/google/doctor">Login as Doctor with Google</a>'

@auth.route("/login/<provider>/<role>")
def login(provider, role):
	nonce = secrets.token_urlsafe(16)
	session["nonce"] = nonce
	
	session["provider"] = provider
	session["role"] = role

	if provider == "google":
		return google.authorize_redirect(url_for("auth.authorize", _external=True), nonce=nonce)

@auth.route("/authorize")
def authorize():
	provider = session.get("provider")
	role = session.get("role", "patient")
	if provider == "google":
		token = google.authorize_access_token()
		nonce = session.pop("nonce", None)

		if nonce is None:
			return "Error: Missing nonce.", 400

		user_info = google.parse_id_token(token, nonce=nonce)

		google_id = user_info.get("sub")
		email = user_info.get("email")
		name = user_info.get("name")

		if role == "patient":
			user = Patient.query.filter_by(sso_user_id=google_id).first()

			if not user:
				existing_user = Patient.query.filter_by(email=email).first()

				if existing_user:
					existing_user.sso_provider = "Google"
					existing_user.sso_user_id = google_id
					db.session.commit()
					user = existing_user
				else:
					user = Patient(email=email, full_name=name, sso_provider="Google", sso_user_id=google_id)
					db.session.add(user)
					db.session.commit()
		elif role == "doctor":
			user = Doctor.query.filter_by(sso_user_id=google_id).first()

			if not user:
				existing_user = Doctor.query.filter_by(email=email).first()

				if existing_user:
					existing_user.sso_provider = "Google"
					existing_user.sso_user_id = google_id
					db.session.commit()
					user = existing_user
				else:
					user = Doctor(email=email, full_name=name, sso_provider="Google", sso_user_id=google_id)
					db.session.add(user)
					db.session.commit()

		login_user(user)
	
	return 'successful'

@auth.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("auth.home"))
