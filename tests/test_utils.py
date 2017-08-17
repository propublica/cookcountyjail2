import os
import pytest


from jailscraper import app_config, utils


def test_s3_url():
    expected = 'https://s3.amazonaws.com/cookcountyjail.il.propublica.org/test/folder/manifest.csv'
    generated = utils.get_s3_url('test/folder/manifest.csv')
    assert generated == expected
