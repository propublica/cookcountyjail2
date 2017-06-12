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

## Contributing

1. Fork this repository.
2. Create a [new issue](https://github.com/propublica/cookcountyjail2/issues/new) if none exists.
3. Create a new branch named `XXXX-short-name` e.g. `0019-document-contributing`, commit your changes to the branch, and push to your fork. (You can use `git push -u` to automatically create the new upstream branch).
4. Create a pull request back to the main repository.

## S3 filesystem structure

```
- </dev/prod>
  - /daily
    - <YYYY-MM-DD>.csv
    - ...
  - /raw
    - <YYYY-MM-DD>-<BOOKING_ID>.html
```

