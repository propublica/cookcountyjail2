import boto3
import csv
import logging
import io
import os
import scrapy

from datetime import date, datetime, timedelta
from jailscraper import project_config
from jailscraper.models import InmatePage
from urllib.parse import urlparse, parse_qs

# Quiet down, Boto!
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)

ONE_DAY = timedelta(days=1)


class InmatesSpider(scrapy.Spider):
    name = "inmates"

    def __init__(self, category=None, *args, **kwargs):
        super(InmatesSpider, self).__init__(*args, **kwargs)
        s3 = boto3.resource('s3')
        self._bucket = s3.Bucket(project_config.S3_BUCKET)
        self._today = datetime.combine(date.today(), datetime.min.time())
        self._yesterday = self._today - ONE_DAY

    def start_requests(self):
        for url in self._generate_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        inmate = InmatePage(response.body)
        self._save_to_s3(response, inmate)
        yield {
            'Age_At_Booking': inmate.age_at_booking,
            'Bail_Amount': inmate.bail_amount,
            'Booking_Date': inmate.booking_date,
            'Booking_Id': inmate.booking_id,
            'Charges': inmate.charges,
            'Court_Date': inmate.court_date,
            'Court_Location': inmate.court_location,
            'Gender': inmate.gender,
            'Inmate_Hash': inmate.inmate_hash,
            'Height': inmate.height,
            'Housing_Location': inmate.housing_location,
            'Race': inmate.race,
            'Weight': inmate.weight,
            'Incomplete': self._is_complete_record(inmate)
        }

    def _generate_urls(self):
        """Make URLs."""
        prefix = '{0}/daily'.format(project_config.TARGET)
        keys = list(self._bucket.objects.filter(Prefix=prefix).all())
        last_file = keys[-1].get()
        lines = last_file[u'Body'].read().split()
        lines = [line.decode('utf-8') for line in lines]
        reader = csv.DictReader(lines)

        urls = []
        for row in reader:
            urls.append(project_config.INMATE_URL_TEMPLATE.format(row['Booking_Id']))

        last_date = keys[-1].key.split('/')[-1].split('.')[0]
        last_date = datetime.strptime(last_date, '%Y-%m-%d')

        self._start_date = last_date

        last_date = last_date + ONE_DAY
        while last_date < self._today:
            next_query = last_date.strftime('%Y-%m%d')
            for num in range(1, project_config.MAX_DEFAULT_JAIL_NUMBER + 1):
                jailnumber = '{0}{1:03d}'.format(next_query, num)
                urls.append(project_config.INMATE_URL_TEMPLATE.format(jailnumber))
            last_date = last_date + ONE_DAY

        return ['http://www2.cookcountysheriff.org/search2/details.asp?jailnumber=2015-0904292']
        return urls[:20000]

    def _save_to_s3(self, response, inmate):
        """Save raw data to s3."""
        key = '{0}/raw/{1}-{2}.html'.format(*[project_config.TARGET,
                                              self._today.strftime('%Y-%m-%d'),
                                              inmate.booking_id
                                             ])
        f = io.BytesIO(response.body)
        upload = self._bucket.upload_fileobj(f, key)
        self.log('Uploaded s3://{0}/{1}'.format(project_config.S3_BUCKET, key))

    def _is_complete_record(self, inmate):
        """Was this scrape run daily?"""
        booking_date = datetime.strptime(inmate.booking_date, '%Y-%m-%d')
        return booking_date > self._start_date and booking_date < self._yesterday
