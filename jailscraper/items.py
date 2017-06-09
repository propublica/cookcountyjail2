# -*- coding: utf-8 -*-
import hashlib
import scrapy

from datetime import datetime
from dateutil.relativedelta import relativedelta


def strip(x):
    """Simple stripping for lists and strings."""
    if isinstance(x, list):
        x = ''.join(x)
    return x.strip().replace(u'\xa0', u' ')


def makedate(x):
    """Turns mm/dd/YYYY into YYYY-mm-dd"""
    x = strip(x)
    return datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d')


class InmateRecordItem(scrapy.Item):
    Booking_Id = scrapy.Field()
    Booking_Date = scrapy.Field()
    Inmate_Hash = scrapy.Field()
    Gender = scrapy.Field(serializer=strip)
    Race = scrapy.Field(serializer=strip)
    Height = scrapy.Field(serializer=strip)
    Weight = scrapy.Field(serializer=strip)
    Age_At_Booking = scrapy.Field()
    Housing_Location = scrapy.Field(serializer=strip)
    Charges = scrapy.Field(serializer=strip)
    Bail_Amount = scrapy.Field(serializer=strip)
    Court_Date = scrapy.Field(serializer=makedate)
    Court_Location = scrapy.Field(serializer=strip)
    Incomplete = scrapy.Field()

    def calculate_booking_age(self, response):
        """Calculate age at booking."""
        birthdate_string = strip(response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[3]//text()').extract())
        birthdate = datetime.strptime(birthdate_string, '%m/%d/%Y')
        bookingdate = datetime.strptime(strip(self['Booking_Date']), '%Y-%m-%d')
        return relativedelta(bookingdate, birthdate).years

    def calculate_inmate_hash(self, response):
        """Hash name, birthdate, race, and gender.

        This hash, while imperfect, allows us to track recidivism to some degree.
        """
        rawname = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[2]//text()').extract()
        name = strip(rawname).replace(' ', '')
        birthdate_raw = response.selector.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[3]//text()').extract()
        birthdate = strip(birthdate_raw).replace('/', '')
        id = '{0}{1}{2}{3}'.format(name, birthdate, self['Race'], self['Gender']).encode('utf-8')
        return hashlib.sha256(id).hexdigest()


