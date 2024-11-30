from functools import lru_cache
from google.cloud import secretmanager
import os

@lru_cache()
def get_secret_client():
    return secretmanager.SecretManagerServiceClient()
def get_secret(secret_id, version_id="latest"):
    GCP_PROJECT = os.environ.get('GCP_PROJECT')
    secret_client = get_secret_client()
    name = f"projects/{GCP_PROJECT}/secrets/{secret_id}/versions/{version_id}"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")