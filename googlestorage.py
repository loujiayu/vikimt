from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()
bucket_name = 'patientstorage'

client = storage.Client()
bucket = client.get_bucket(bucket_name)
blobs = bucket.list_blobs()

print(f"Access granted to bucket '{bucket_name}':")
for blob in blobs:
		print(blob.name)
