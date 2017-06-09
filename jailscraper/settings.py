# -*- coding: utf-8 -*-

# Scrapy settings; see https://doc.scrapy.org/en/latest/topics/settings.html#

BOT_NAME = 'jailscraper'

SPIDER_MODULES = ['jailscraper.spiders']
NEWSPIDER_MODULE = 'jailscraper.spiders'

RETRY_ENABLED = False
USER_AGENT = 'ProPublica Cook County Jail Scraper - contact david.eads@propublica.org for details'
COOKIES_ENABLED = False
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 12

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_TARGET_CONCURRENCY = 12.0
