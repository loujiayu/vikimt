# AI Service configurations
AI_SERVICE_CONFIG = {
    "gemini": {
        "project": "viki-419417",
        "location": "us-central1",
        "model_name": "gemini-2.0-flash-001",
        "temperature": 1.0,
        "top_p": 0.95,
        "max_output_tokens": 1024,
        "safety_settings": [
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "OFF"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "OFF"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "OFF"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "OFF"}
        ]
    }
    # Add configurations for other AI services here
}
