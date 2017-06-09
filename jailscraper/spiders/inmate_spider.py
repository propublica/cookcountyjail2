import boto3
import csv
import logging
import io
import os
import scrapy

from datetime import date, datetime, timedelta
from jailscraper import project_config
from jailscraper.items import InmateRecordItem
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
        inmate = self._create_inmate(response)
        self._save_to_s3(response, inmate)
        yield inmate

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

        # last_date = last_date + ONE_DAY
        # while last_date < self._today:
            # next_query = last_date.strftime('%Y-%m%d')
            # for num in range(1, project_config.MAX_DEFAULT_JAIL_NUMBER + 1):
                # jailnumber = '{0}{1:03d}'.format(next_query, num)
                # urls.append(project_config.INMATE_URL_TEMPLATE.format(jailnumber))
            # last_date = last_date + ONE_DAY

        return urls

    def _save_to_s3(self, response, inmate):
        """Save raw data to s3."""
        key = '{0}/raw/{1}-{2}.html'.format(*[project_config.TARGET,
                                              self._today.strftime('%Y-%m-%d'),
                                              inmate['Booking_Id']
                                             ])
        f = io.BytesIO(response.body)
        upload = self._bucket.upload_fileobj(f, key)
        self.log('Uploaded s3://{0}/{1}'.format(project_config.S3_BUCKET, key))

    def _create_inmate(self, response):
        """Does the heavy lifting of parsing and creating an inmate."""
        inmate = InmateRecordItem()

        booking_id = self._parse_booking_id(response)

        booking_date_string = booking_id[:9]
        booking_date = datetime.strptime(booking_date_string, '%Y-%m%d')

        if booking_date > self._start_date and booking_date < self._yesterday:
            inmate['Incomplete'] = True
        else:
            inmate['Incomplete'] = False

        inmate['Bail_Amount'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[4]//text()').extract()
        inmate['Booking_Date'] = booking_date.strftime('%Y-%m-%d')
        inmate['Booking_Id'] = booking_id
        inmate['Charges'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[4]/td[1]//text()').extract()
        inmate['Court_Date'] = response.selector.xpath('//div[@id="mainContent"]/table[3]/tr[2]/td[1]//text()').extract()
        inmate['Court_Location'] = response.selector.xpath('//div[@id="mainContent"]/table[3]/tr[2]/td[2]//text()').extract()
        inmate['Gender'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[5]//text()').extract()
        inmate['Height'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[6]//text()').extract()
        inmate['Housing_Location'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[2]//text()').extract()
        inmate['Race'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[4]//text()').extract()
        inmate['Weight'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[7]//text()').extract()

        inmate['Age_At_Booking'] = inmate.calculate_booking_age(response)
        inmate['Inmate_Hash'] = inmate.calculate_inmate_hash(response)

        return inmate

    def _parse_booking_id(self, response):
        parsed_url = urlparse(response.url)
        qs = parse_qs(parsed_url.query)
        return qs['jailnumber'][0]
