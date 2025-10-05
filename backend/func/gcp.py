from google.cloud import storage
import os

def upload_file_to_gcp(local_path: str, gcp_path=None, gcs_bucket_name: str=os.environ.get("GCS_BUCKET_NAME")):
    if gcp_path is None:
        gcp_path = os.path.basename(local_path)

    client = storage.Client()
    bucket = client.bucket(gcs_bucket_name)
    
    blob = bucket.blob(gcp_path)
    blob.upload_from_filename(local_path)
    public_url = blob.public_url
    return public_url