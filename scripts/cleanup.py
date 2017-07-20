#!/usr/bin/env python
import boto3
import csv
import logging
from io import StringIO
from jailscraper import app_config

logging.basicConfig()
logger = logging.getLogger(app_config.PROJECT_SLUG)
logger.setLevel(logging.DEBUG)

PUBLIC_READ_URI = 'http://acs.amazonaws.com/groups/global/AllUsers'
PUBLIC_READ_PERMISSION = 'READ'


def cleanup():
    """
    Set all urls to public read. Returns list of URLs found.
    """
    urls = []
    client = boto3.client('s3')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(app_config.S3_BUCKET)
    prefix = '{0}/daily'.format(app_config.TARGET)
    keys = list(bucket.objects.filter(Prefix=prefix).all())
    for key in keys:
        acl = key.Acl()
        publicread_perms = [grant for grant in acl.grants
                            if grant['Grantee'].get('URI') == PUBLIC_READ_URI and
                            grant['Permission'] == PUBLIC_READ_PERMISSION]

        url = client.generate_presigned_url('get_object', Params={'Bucket': app_config.S3_BUCKET, 'Key': key.key})
        urls.append((url.split('?')[0],))

        if not len(publicread_perms):
            logger.debug('{0}/{1} set to public-read'.format(key.bucket_name, key.key))
            key.Acl().put(ACL='public-read')
        else:
            logger.debug('{0}/{1} is already public read'.format(key.bucket_name, key.key))

    return urls


def write_urls(urls):
    """
    Write URLs to manifest file on S3.
    """
    urls = sorted(urls)  # Sort in case Amazon order changes for some reason
    f = StringIO()
    writer = csv.writer(f)
    writer.writerows(urls)
    s3 = boto3.resource('s3')
    path = '{0}/manifest.csv'.format(app_config.TARGET)
    if path.startswith('/'):
        path = path[1:]
    key = s3.Object(app_config.S3_BUCKET, path)
    key.put(Body=f.getvalue())
    key.Acl().put(ACL='public-read')


if __name__ == '__main__':
    urls = cleanup()
    write_urls(urls)
