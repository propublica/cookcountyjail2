#!/bin/bash

scrapy crawl inmates -t csv -o s3://cookcountyjail.il.propublica.org/daily/`date +"%Y-%m-%d" -d "yesterday"`.csv

scripts/cleanup.py
