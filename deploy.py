import pulumi
import pulumi_gcp as gcp
from pulumi import Config

# Get configuration
config = Config()
project = config.require('project')
region = config.get('region') or 'us-central1'



# Enable the Required Services

required_services = {
    "secret-manager-api": "secretmanager.googleapis.com"
}
for key, service in required_services.items():
    gcp.projects.Service(
        key,
        service=service
    )

# Create a service account for the Cloud Function
function_sa = gcp.serviceaccount.Account('weather-monitor-sa',
    account_id='weather-monitor-sa',
    display_name='weather Monitor Service Account',
    project=project)

# Grant required roles to the service account
function_sa_roles = [
    'roles/cloudfunctions.invoker',
    'roles/logging.logWriter'
]

for role in function_sa_roles:
    sa_iam_binding = gcp.projects.IAMBinding(f'weather-monitor-sa-{role.split("/")[-1]}',
        project=project,
        role=role,
        members=[pulumi.Output.concat('serviceAccount:', function_sa.email)])

# Create a storage bucket for the function source
bucket = gcp.storage.Bucket('weather-monitor-bucket',
    location=region,
    force_destroy=True)

# Create a bucket object containing the function source
bucket_object = gcp.storage.BucketObject('weather-monitor-function-source',
    bucket=bucket.name,
    source=pulumi.FileArchive('./src'))

# Create the Cloud Function
function = gcp.cloudfunctionsv2.Function('weather-monitor',
    name='weather-monitor',
    location=region,
    description='Checks weather and runs IFTTT notification',
    build_config={
        'runtime':'python312',
        'entry_point':'check_weather',
        'source':{
            'storage_source':{
                'bucket':bucket.name,
                'object':bucket_object.name
            }
        }
    },
    service_config={
        'max_instance_count':1,
        'available_memory':'256Mi',
        'timeout_seconds':60,
        'service_account_email':function_sa.email,
        'ingress_settings':'ALLOW_ALL',
        'environment_variables':{
            'WEATHER_LAT':config.get('weather_lat') or '40.7128',
            'WEATHER_LON':config.get('weather_lon') or '-74.0060',
            'GCP_PROJECT':config.get('gcp:project')
        }
    }
)

existing_function = gcp.cloudfunctionsv2.get_function(
    name="weather-monitor",
    location=region
)
if existing_function:
    function_url = existing_function.url

    
# Export the function URL
pulumi.export("function_url", function_url)

# Create a service account for the Cloud Scheduler
scheduler_account = gcp.serviceaccount.Account('scheduler-account',
    account_id='weather-scheduler',
    display_name='weather Monitor Scheduler')

# Create Cloud Scheduler job
scheduler = gcp.cloudscheduler.Job('weather-monitor-scheduler',
    name='weather-monitor-job',
    description='Triggers the weather monitoring function every 30 minutes',
    schedule='*/30 * * * *',
    time_zone='UTC',
    region=region,
    http_target={
        "uri": function_url,
        "http_method": "POST",
        "oidc_token": {
            "audience": function_url,
            "service_account_email": scheduler_account.email,
        },
    },
    opts=pulumi.ResourceOptions(depends_on=[function])
)

