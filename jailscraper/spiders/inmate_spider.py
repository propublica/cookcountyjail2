import csv
import os
import scrapy

from datetime import date, timedelta
from urllib.parse import urlparse, parse_qs

ONE_DAY = timedelta(days=1)
INITIAL_DATA_FILE = 'data/raw_inmate_data/2016-07-24.csv'
URL_TEMPLATE = 'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber={0}'

class InmatesSpider(scrapy.Spider):
    name = "inmates"

    def __init__(self, category=None, *args, **kwargs):
        super(InmatesSpider, self).__init__(*args, **kwargs)
        self._today = date.today()
        self._yesterday = date.today() - ONE_DAY
        self._make_scrape_dir()
        self._last_scraped_data = self._get_scraped_data()

    def _make_scrape_dir(self):
        self._data_dir = 'data/scraped_html/{0}'.format(self._today.strftime('%Y-%m-%d'))
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)

    def _get_scraped_data(self):
        """
        Get data from last scrape
        """
        yesterdays_file = 'data/raw_inmate_data/{0}.csv'.format(self._yesterday.strftime('%Y-%m-%d'))

        if not os.path.exists(yesterdays_file):
            yesterdays_file = INITIAL_DATA_FILE
            # @TODO if this path is taken, we need to crank through the intervening period

        with open(yesterdays_file) as f:
            reader = csv.DictReader(f)

            # @TODO make urls here
            return list(reader)

    def start_requests(self):
        for row in self._last_scraped_data:
            url = URL_TEMPLATE.format(row['Booking_Id'])
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        parsed_url = urlparse(response.url)
        qs = parse_qs(parsed_url.query)
        filename = '{0}/{1}.html'.format(self._data_dir, qs['jailnumber'][0])
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {0}'.format(filename))
