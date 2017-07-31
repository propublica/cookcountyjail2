"""
Spider to fetch active inmate entries
"""
import boto3
import csv
import logging
import io
import os
import requests
import scrapy

from datetime import date, datetime, timedelta
from jailscraper import app_config
from jailscraper.models import InmatePage

# Quiet down, Boto! & s3transfer
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)

_LOCAL_FILES_DIR = 'data/daily'
_LOCAL_RAW_DATA_DIR = 'data/raw'
ONE_DAY = timedelta(days=1)


class InmatesSpider(scrapy.Spider):
    name = "inmates"

    def __init__(self, category=None, *args, **kwargs):
        super(InmatesSpider, self).__init__(*args, **kwargs)
        if app_config.USE_S3_STORAGE:
            s3 = boto3.resource('s3')
            self._bucket = s3.Bucket(app_config.S3_BUCKET)
        self._today = datetime.combine(date.today(), datetime.min.time())
        self._yesterday = self._today - ONE_DAY

    def parse(self, response):
        inmate = InmatePage(response.body)

        if app_config.USE_LOCAL_STORAGE:
            self._save_local(response, inmate)

        if app_config.USE_S3_STORAGE:
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

    def start_requests(self):
        for url in self._generate_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def _existing_inmate_urls(self):
        next_date, has_ids, f = self._get_seed_file()
        next_date = _to_datetime(next_date)
        if has_ids:
            next_date += ONE_DAY
            reader = csv.DictReader(f)
            previous_ids = (
                app_config.INMATE_URL_TEMPLATE.format(row['Booking_Id'])
                for row in reader
            )
        else:
            previous_ids = iter([])
        return next_date, previous_ids

    def _generate_page_filename(self, inmate):
        """Make a scraped page filename."""
        name = '{0}-{1}.html'.format(self._today.strftime('%Y-%m-%d'), inmate.booking_id)
        return name

    def _generate_urls(self):
        """Make URLs."""
        next_date, existing_inmate_urls = self._existing_inmate_urls()

        for url in existing_inmate_urls:
            yield url

        # Scan the universe of URLs
        while next_date < self._today:
            cur_day_query = next_date.strftime('%Y-%m%d')
            next_date += ONE_DAY
            for num in _daily_booked_nums():
                jail_id_number = '{0}{1:03d}'.format(cur_day_query, num)
                yield app_config.INMATE_URL_TEMPLATE.format(jail_id_number)

    def _get_local_seed_file(self):
        """Get seed file from local file system. Return array of lines."""

        found_non_empty_file = False
        for file_name in reversed(_get_local_files()):
            last_file = os.path.join(_LOCAL_FILES_DIR, file_name)
            found_non_empty_file = bool(os.path.getsize(last_file))
            if found_non_empty_file:
                self.log('Used {0} from local file system to seed scrape.'.format(last_file))
                last_date = file_name.split('.')[0]
                f = open(last_file)
                break
        else:
            self.log('No seed file or no non-empty file found.')
            last_date = app_config.FALLBACK_START_DATE
            f = io.StringIO(None)
        return last_date, found_non_empty_file, f

    def _get_seed_file(self):
        """Returns data from seed file as array of lines."""
        if app_config.USE_S3_STORAGE:
            func = self._get_s3_seed_file
        else:
            func = self._get_local_seed_file
        return func()

    def _get_s3_seed_file(self):
        """Get seed file from S3. Return last date and array of lines."""

        target = app_config.TARGET
        if target:
            target = '{0}/'.format(target)

        url = "https://s3.amazonaws.com/{0}/{1}manifest.csv".format(app_config.S3_BUCKET, target)
        resp = requests.get(url)

        # For now, this "csv" is just a list of filenames, so we don't even need to parse as csv.
        seed_url = resp.text.splitlines().pop()
        last_date = seed_url.split('/')[-1].split('.')[0]
        seed_response = requests.get(seed_url)
        self.log('Used {0} from S3 file system to seed scrape.'.format(seed_url))
        return last_date, bool(len(seed_response.text)), io.StringIO(seed_response.text)

    def _is_complete_record(self, inmate):
        """Was this scrape run daily?"""
        booking_date = datetime.strptime(inmate.booking_date, '%Y-%m-%d')
        return booking_date < self._yesterday

    def _save_local(self, response, inmate):
        """Save scraped page to local filesystem."""
        os.makedirs(_LOCAL_RAW_DATA_DIR, exist_ok=True)
        filepath = os.path.join(_LOCAL_RAW_DATA_DIR, self._generate_page_filename(inmate))
        with open(filepath, 'wb') as f:
            f.write(response.body)
        self.log('Wrote {0} to local file system'.format(filepath))

    def _save_to_s3(self, response, inmate):
        """Save scraped page to s3."""
        key = '{0}/raw/{1}'.format(app_config.TARGET, self._generate_page_filename(inmate))
        if key.startswith('/'):
            key = key[1:]
        f = io.BytesIO(response.body)
        self._bucket.upload_fileobj(f, key)
        self.log('Uploaded s3://{0}/{1}'.format(app_config.S3_BUCKET, key))


def _daily_booked_nums():
    return range(1, app_config.MAX_DEFAULT_JAIL_NUMBER + 1)


def _get_local_files():
    try:
        files = sorted(os.listdir(_LOCAL_FILES_DIR))
    except FileNotFoundError:
        files = []
    return files


def _to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')
