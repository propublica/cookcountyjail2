# Cook County Jail Inmate Scraper (version 2)

Descended in spirit from the Supreme Chi-Town Coding Crew scraper/API that ran from 2014-2016.

## Installing

Create a Python virtual environment, then:

```
pip install -r requirements.txt
```

## Setting up environment

Get configuration variables:

```
source env.sh
```

More TK

## Running the scraper

```
scrapy crawl inmates
```

## S3 filesystem structure

```
- </dev/prod>
  - /daily
    - <YYYY-MM-DD>.csv
    - ...
  - /raw
    - <YYYY-MM-DD>-<BOOKING_ID>.html
```


