from google.cloud import storage

import logging
logging.basicConfig(level=logging.INFO)

def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str) -> bool:
  """Uploads a file to the bucket."""
  storage_client: storage.Client = storage.Client()
  bucket: storage.Bucket  = storage_client.get_bucket(bucket_name)
  blob: storage.Blob = bucket.blob(destination_blob_name)
  blob.upload_from_filename(source_file_name)
  logging.info(f"File uploaded to {destination_blob_name}")
  return True
