# Cook County Jail Inmate Scraper (version 2)

Scrapes the Cook County Jail Inmate locator to create a database of inmate records for analysis.

Descended in spirit from the Supreme Chi-Town Coding Crew scraper/API that ran from 2014-2016.

## Installing

Clone the repository, then install requirements:

```
pip install -r requirements.txt
```

As always, `virtualenv` and `virtualenv-wrapper` are highly recommended.

## Setting up environment (optional)

All project-specific configuration options are available in `jailscraper/app_config.py`.

Instead of directly editing this file, you are encouraged to use environment variables instead.

Environment variables can be used to enable S3 storage or change core settings without having to change (and track changes to) `jailscraper/app_config.py`.

An example environment file is bundled with the repo. To enable:
```
cp env.sh.example env.sh
source env.sh
```

## Running the scraper

```
scrapy crawl inmates -o myscrape.csv -t csv
```

If local storage is enabled (as it is by default), every scraped page will be saved to `data/raw`.

## Contributing

1. Fork this repository.
2. Create a [new issue](https://github.com/propublica/cookcountyjail2/issues/new) if none exists.
3. Create a new branch named `XXXX-short-name` e.g. `0019-document-contributing`, commit your changes to the branch, and push to your fork. (You can use `git push -u origin XXXX-short-name` to automatically create the new upstream branch).
4. Create a pull request back to the main repository.

## Scraper filesystem structure

This is likely to change somewhat.

```
- </dev/prod>
  - /daily
    - <YYYY-MM-DD>.csv
    - ...
  - /raw
    - <YYYY-MM-DD>-<BOOKING_ID>.html
```

## Roadmap

When the scraper is running in production, we will release the daily snapshots.
