from imp import reload
from jailscraper import app_config


def test_s3_url(monkeypatch):
    monkeypatch.setenv('{0}_TARGET'.format(app_config.PROJECT_SLUG), 'dev')
    monkeypatch.setenv('{0}_S3_BUCKET'.format(app_config.PROJECT_SLUG), 'TESTBUCKET')
    reload(app_config)
    from jailscraper import utils
    expected = 'https://s3.amazonaws.com/TESTBUCKET/dev/folder/manifest.csv'
    generated = utils.get_s3_url('folder/manifest.csv')
    assert generated == expected
