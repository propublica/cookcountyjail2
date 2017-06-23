#!/usr/bin/env python
import boto3
import logging
from jailscraper import app_config

logging.basicConfig()
logger = logging.getLogger(app_config.PROJECT_SLUG)
logger.setLevel(logging.DEBUG)

PUBLIC_READ_URI = 'http://acs.amazonaws.com/groups/global/AllUsers'
PUBLIC_READ_PERMISSION = 'READ'


def cleanup():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(app_config.S3_BUCKET)
    prefix = '{0}/daily'.format(app_config.TARGET)
    keys = list(bucket.objects.filter(Prefix=prefix).all())
    for key in keys:
        acl = key.Acl()
        publicread_perms = [grant for grant in acl.grants
                            if grant['Grantee'].get('URI') == PUBLIC_READ_URI and
                            grant['Permission'] == PUBLIC_READ_PERMISSION]

        if not len(publicread_perms):
            logger.debug('{0}/{1} set to public-read'.format(key.bucket_name, key.key))
            key.Acl().put(ACL='public-read')
        else:
            logger.debug('{0}/{1} is already public read'.format(key.bucket_name, key.key))


if __name__ == '__main__':
    cleanup()
