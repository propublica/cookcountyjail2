import csv
import requests

from jailscraper import app_config

S3_ROOT = 'https://s3.amazonaws.com'


def get_s3_url(path):
    target = app_config.TARGET
    if target: '{0}/'.format(target)
    return "{0}/{1}/{2}{3}".format(S3_ROOT, app_config.S3_BUCKET, target, path)


def get_manifest():
    resp = requests.get(get_s3_url('manifest.csv'))
    lines = resp.text.splitlines()
    return sorted(lines)
