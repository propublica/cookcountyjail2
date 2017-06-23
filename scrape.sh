#!/bin/bash

scrapy crawl inmates -t csv -o s3://cookcountyjail.il.propublica.org/dev/daily/`date +"%Y-%m-%d"`.csv

scripts/cleanup.py
