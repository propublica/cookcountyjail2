import csv
import os
import scrapy

from datetime import date, timedelta
from jailscraper import project_config
from jailscraper.items import InmateRecordItem
from urllib.parse import urlparse, parse_qs

ONE_DAY = timedelta(days=1)


class InmatesSpider(scrapy.Spider):
    name = "inmates"

    def start_requests(self):
        urls = [
            'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber=2017-0531001'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        inmate = InmateRecordItem()
        inmate['Booking_Id'] = self._parse_booking_id(response)
        inmate['Booking_Date'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[1]//text()').extract()
        inmate['Race'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[4]//text()').extract()
        inmate['Height'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[6]//text()').extract()
        inmate['Weight'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[7]//text()').extract()
        inmate['Gender'] = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[5]//text()').extract()
        inmate['Housing_Location'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[2]//text()').extract()
        inmate['Bail_Amount'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[4]//text()').extract()
        inmate['Charges'] = response.selector.xpath('//div[@id="mainContent"]/table[2]/tr[4]/td[1]//text()').extract()
        inmate['Court_Date'] = response.selector.xpath('//div[@id="mainContent"]/table[3]/tr[2]/td[1]//text()').extract()
        inmate['Court_Location'] = response.selector.xpath('//div[@id="mainContent"]/table[3]/tr[2]/td[2]//text()').extract()
        yield inmate

    def _parse_booking_id(self, response):
        parsed_url = urlparse(response.url)
        qs = parse_qs(parsed_url.query)
        return qs['jailnumber']
