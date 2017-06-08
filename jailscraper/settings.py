# -*- coding: utf-8 -*-

# Scrapy settings; see https://doc.scrapy.org/en/latest/topics/settings.html#

BOT_NAME = 'jailscraper'

SPIDER_MODULES = ['jailscraper.spiders']
NEWSPIDER_MODULE = 'jailscraper.spiders'

RETRY_ENABLED = False
USER_AGENT = 'ProPublica Cook County Jail Scraper'
COOKIES_ENABLED = False
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
