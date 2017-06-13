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


SECRETS = get_secrets()
S3_BUCKET = SECRETS['S3_BUCKET']
TARGET = SECRETS['TARGET']
S3_URL = 's3://{0}/{1}'.format(SECRETS['S3_BUCKET'], SECRETS['TARGET'])
