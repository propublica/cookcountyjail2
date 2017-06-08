# -*- coding: utf-8 -*-
import dateparser
import scrapy

def strip(x):
    if isinstance(x, list):
        x = ''.join(x)
    return x.strip()

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
    Court_Date = scrapy.Field(serializer=strip)
    Court_Location = scrapy.Field(serializer=strip)
