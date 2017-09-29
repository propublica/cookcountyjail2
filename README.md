# Cook County Jail Inmate Scraper (version 2)

Scrapes the Cook County Jail Inmate locator to create a database of inmate records for analysis.

Descended in spirit from the Supreme Chi-Town Coding Crew scraper/API that ran from 2014-2016.

If you find this software useful, sign up for [ProPublica's newsletters](http://go.propublica.org/sign-up) and consider [donating to ProPublica Illinois](https://www.propublica.org/donate-illinois).

## Requirements

* Python 3.6+
* (Optional) Amazon S3

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

```
- </dev/prod>
  - /daily
    - <YYYY-MM-DD>.csv
    - ...
  - /raw
    - <YYYY-MM-DD>-<BOOKING_ID>.html
```

## Data structure of CSVs

* `age_at_booking`: Age in years calculated from birthdate and booking date.
* `bail_amount`: Bond amount at time of scrape.
* `booking_id`: Unique ID for an inmate's stay in the jail.
* `charges`: ILCS charges associated with this inmate. This is typically the "lead" charge, but is less reliable than other fields in this dataset. Inmates may have many charges and the most serious charge is not guaranteed to be input into the Sheriff's system.
* `court_date`: Next court date as of scrape date.
* `court_location`: Next court location as of scrape date.
* `gender`: Gender ('male', 'female', 'transgender').
* `height`: Height in feet and inches (e.g. '503').
* `housing_location`: Housing location as of scrape date (e.g. 'DIV2-D1-D-32').
* `inmate_hash`: A not truly unique hash generated from personal details to track recidivism.
* `race`: Race (e.g. 'LT').
* `weight`: Weight in pounds.

## Scripts

To run scripts, set the `PYTHONPATH` from the top directory.

```bash
export PYTHONPATH=`pwd`:$PYTHONPATH
```

### `scripts/cleanup.py`

Run this script to set the ACLs on daily snapshots to `public-read` and to create a file manifest.
