from utils.secrets import get_secret
import requests

def handle_snow() -> bool:
    ifttt_webhook_url = get_secret("SNOW_WEBHOOK_URL")

    response = requests.get(ifttt_webhook_url)
    if response.status_code != 200:
        response.raise_for_status()
    return True