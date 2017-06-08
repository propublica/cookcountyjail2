"""ProPublica specific configuration and utilities"""
import os

PROJECT_SLUG = 'cookcountyjail2'
INMATE_URL_TEMPLATE = 'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber={0}'

"""Sets the maximum jail number to scan for by default.

If the subsequent jail number returns a 2xx status code, it will be incremented
until an error code is sent. [@TODO: Not implemented, see
https://github.com/propublica/cookcountyjail2/issues/9]
"""
MAX_DEFAULT_JAIL_NUMBER = 400


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
S3_URL = '{0}/{1}'.format(SECRETS['S3_BUCKET'], SECRETS['TARGET'])
