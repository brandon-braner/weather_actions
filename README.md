# Snow Monitor

A GCP Cloud Function that checks for weather conditions using the OpenWeatherMap API and sends notifications via IFTTT.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up required secrets in GitHub:
- `GCP_SA_KEY`: Google Cloud Service Account key with necessary permissions
- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `PULUMI_ACCESS_TOKEN`: Your Pulumi access token
- `PULUMI_CONFIG_PASSPHRASE`: Passphrase for Pulumi config encryption
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key

3. Initialize Pulumi:
```bash
pulumi stack init dev
pulumi config set gcp:project YOUR_PROJECT_ID
pulumi config set weather_lat YOUR_LATITUDE  # Optional, defaults to NYC
pulumi config set weather_lon YOUR_LONGITUDE # Optional, defaults to NYC
```

4. Deploy:
The application will automatically deploy when you push to the main branch, or you can deploy manually:
```bash
pulumi up
```

## Architecture

- The application runs as a GCP Cloud Function
- Cloud Scheduler triggers the function every 30 minutes
- The function checks OpenWeatherMap API for snow conditions
- If snow is detected, it triggers an IFTTT webhook (to be implemented)

## Local Development

To test locally:
```bash
functions-framework --target check_weather
```
