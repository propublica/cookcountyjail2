"""ProPublica specific configuration and utilities"""
import boto3
import botocore
import logging
import os

# Short name of project, for use in deployment and credential juggling.
PROJECT_SLUG = 'cookcountyjail2'


### Helpers

logging.basicConfig()
logger = logging.getLogger(PROJECT_SLUG)
logger.setLevel(logging.INFO)

logger.info('Loading {0} config'.format(PROJECT_SLUG))


def get_env():
    """Get all environment variables associated with this project.

    Reads environment variables that start with PROJECT_SLUG, strips out the slug
    and adds them to a dictionary.
    """
    env = {}
    for k, v in os.environ.items():
        if k.startswith(PROJECT_SLUG):
            new_k = k[len(PROJECT_SLUG) + 1:]
            env[new_k] = v

    return env


### Config

ENVIRONMENT = get_env()

# URL template for inmate lookup tool.
INMATE_URL_TEMPLATE = 'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber={0}'

# Default maximum jail number to scan for a on a given day. This is a soft max (@TODO not implement).
MAX_DEFAULT_JAIL_NUMBER = ENVIRONMENT.get('MAX_DEFAULT_JAIL_NUMBER', 400)

# Environment name (e.g. 'dev', 'prod')
TARGET = ENVIRONMENT.get('TARGET')

# Use S3 storage to mirror scraped pages. Must be set in env.sh. Default: false.
USE_S3_STORAGE = bool(ENVIRONMENT.get('USE_S3_STORAGE'), False)
if USE_S3_STORAGE:
    S3_BUCKET = ENVIRONMENT.get('S3_BUCKET')

# Use local storage to mirror scraped pages. Default: true.
USE_LOCAL_STORAGE = bool(ENVIRONMENT.get('USE_LOCAL_STORAGE'), True)

FALLBACK_START_DATE = ENVIRONMENT.get('FALLBACK_START_DATE', '2016-01-01')

# Check for S3 access / @TODO factor into function and test
if S3_BUCKET and USE_S3_STORAGE:
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=S3_BUCKET)
    except botocore.exceptions.ClientError:
        logger.warning('Amazon Web Services is unreachable. Scraped pages will not be stored on Amazon S3.')
        if not USE_LOCAL_STORAGE:
            logger.warning('`USE_LOCAL_STORAGE` is disabled in `app_config.py` and S3 access is failing. Scraped pages will not be stored.')
        USE_S3_STORAGE = False