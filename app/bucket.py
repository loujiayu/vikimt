from flask_restful import Resource
from flask import jsonify
from google.cloud import storage
from flask_login import login_user, logout_user, login_required
import json

client = storage.Client()
GCS_BUCKET_NAME = "patientstorage"

def get_chat_history_from_gcs(patient_id):
		bucket = client.get_bucket(GCS_BUCKET_NAME)
		blob_name = f"{patient_id}/patient"
		blob = bucket.blob(blob_name)

		if not blob.exists():
				return None

		data = blob.download_as_text()
		chat_history = json.loads(data)
		return chat_history

class ChatHistoryResource(Resource):
	@login_required
	def get(self, patient_id):
		chat_history = get_chat_history_from_gcs(patient_id)
		if not chat_history:
				return {'message': 'No chat history found for this patient.'}, 404
		
		return jsonify(chat_history)

