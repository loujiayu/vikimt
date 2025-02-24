from google.cloud import storage

class GCSService:
	def __init__(self, bucket_name):
		self.client = storage.Client()
		self.bucket = self.client.bucket(bucket_name)

	def upload_text(self, text_content, destination_blob_name):
		"""Uploads a text string as a file to the bucket."""
		blob = self.bucket.blob(destination_blob_name)
		blob.upload_from_string(text_content, content_type="text/plain")
		return f"Text uploaded to {destination_blob_name}."

	def download_text(self, source_blob_name):
		"""Downloads a text file from the bucket and returns its content."""		
		blob = self.bucket.blob(source_blob_name)
		if not blob.exists():
			return None
		return blob.download_as_text()

	def list_files(self):
		"""Lists all files in the bucket."""
		return [blob.name for blob in self.bucket.list_blobs()]

	def delete_file(self, blob_name):
		"""Deletes a file from the bucket."""
		blob = self.bucket.blob(blob_name)
		blob.delete()
		return f"Blob {blob_name} deleted."
