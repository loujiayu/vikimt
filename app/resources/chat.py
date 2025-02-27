from flask_restful import Resource
from flask_login import login_user, logout_user, login_required
from flask import jsonify, request
from google import genai
from google.genai import types
from app.gcs_service import GCSService
import logging

client = genai.Client(
		vertexai=True,
		project="viki-419417",
		location="us-central1",
)

def convert_ui_payload_to_contents(ui_payload):
		role_mapping = {
				"assistant": "model",
				"user": "user"
		}
		
		contents = [
				types.Content(
						role=role_mapping[item["type"]],
						parts=[types.Part.from_text(text=item["content"])]
				)
				for item in ui_payload
		]
		
		return contents

class ChatAPI(Resource):
	def __init__(self):
		self.gcs_service = GCSService("patientstorage")

	@login_required
	def post(self, patient_id):
		try:
			data = request.get_json()
			messages = data.get("messages", [])

			if not messages:
				return {"error": "No messages provided"}, 400
			
			# Fetch system_instruction from Google Cloud Storage
			system_instruction_blob = f"{patient_id}/system_instruction.txt"
			system_instruction = self.gcs_service.download_text(system_instruction_blob)
			if not system_instruction:
				system_instruction = "You are a helpful assistant."
			
			logging.info(f"System instruction: {system_instruction}")

			# Convert UI payload to Gemini content format
			contents = convert_ui_payload_to_contents(messages)

			# Define model and configuration
			model_name = "gemini-2.0-flash-001"
			generate_content_config = types.GenerateContentConfig(
					temperature=1,
					top_p=0.95,
					max_output_tokens=1024,
					response_modalities=["TEXT"],
					safety_settings=[
							types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
							types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
							types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
							types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
					],
					system_instruction=system_instruction  # Add system instruction
			)

			# Generate response from Gemini AI
			response_text = ""
			logging.info("start generate_content_stream")
			for chunk in client.models.generate_content_stream(
					model=model_name,
					contents=contents,
					config=generate_content_config,
			):
				logging.info(chunk.text)
				response_text += chunk.text

			return jsonify({"message": response_text}), 200

		except Exception as e:
				return {"error": str(e)}, 500