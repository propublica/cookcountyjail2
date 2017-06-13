"""ProPublica specific configuration and utilities"""
import boto3
import botocore
import os


### Helpers

def get_secrets():
    """Get all environment variables associated with this project.

    Reads environment variables that start with PROJECT_SLUG, strips out the slug
    and adds them to a dictionary.
    """
    secrets = {}
    for k, v in os.environ.items():
        if k.startswith(PROJECT_SLUG):
            new_k = k[len(PROJECT_SLUG) + 1:]
            secrets[new_k] = v

    return secrets


### Config

# Shortname of project, for use in deployment and credential juggling.
PROJECT_SLUG = 'cookcountyjail2'

# URL template for inmate lookup tool.
INMATE_URL_TEMPLATE = 'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber={0}'

"""Sets the maximum jail number to scan for by default.

If the subsequent jail number returns a 2xx status code, it will be incremented
until an error code is sent. [@TODO: Not implemented, see
https://github.com/propublica/cookcountyjail2/issues/9]
"""
MAX_DEFAULT_JAIL_NUMBER = 400

# Secrets
SECRETS = get_secrets()
S3_BUCKET = SECRETS.get('S3_BUCKET')
TARGET = SECRETS.get('TARGET')
USE_S3_STORAGE = True
USE_LOCAL_STORAGE = True

# Check for S3 access
if S3_BUCKET and USE_S3_STORAGE:
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=S3_BUCKET)
    except botocore.exceptions.ClientError:
        # @TODO Complain!
        USE_S3_STORAGE = False
