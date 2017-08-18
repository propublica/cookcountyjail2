import os
import pytest

from imp import reload
from jailscraper import app_config


def test_disable_local_storage_with_string(monkeypatch):
    monkeypatch.setenv('{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG), 'fAlse')
    reload(app_config)
    assert not app_config.USE_LOCAL_STORAGE


def test_disable_local_storage_with_zero(monkeypatch):
    monkeypatch.setenv('{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG), '0')
    reload(app_config)
    assert not app_config.USE_LOCAL_STORAGE


def test_enable_local_storage_with_string(monkeypatch):
    monkeypatch.setenv('{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG), "tRue")
    reload(app_config)
    assert app_config.USE_LOCAL_STORAGE


def test_enable_local_storage_with_one(monkeypatch):
    monkeypatch.setenv('{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG), "1")
    reload(app_config)
    assert app_config.USE_LOCAL_STORAGE


def test_default_local_storage(monkeypatch):
    monkeypatch.delenv('{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG), raising=False)
    reload(app_config)
    assert app_config.USE_LOCAL_STORAGE


def test_default_s3_storage(monkeypatch):
    monkeypatch.delenv('{0}_USE_S3_STORAGE'.format(app_config.PROJECT_SLUG), raising=False)
    reload(app_config)
    assert not app_config.USE_S3_STORAGE


def test_jail_number(monkeypatch):
    monkeypatch.setenv('{0}_MAX_DEFAULT_JAIL_NUMBER'.format(app_config.PROJECT_SLUG), "200")
    reload(app_config)
    assert app_config.MAX_DEFAULT_JAIL_NUMBER == 200


def test_target(monkeypatch):
    monkeypatch.setenv('{0}_TARGET'.format(app_config.PROJECT_SLUG), 'prod')
    reload(app_config)
    assert app_config.TARGET == 'prod'


def test_s3_bucket(monkeypatch):
    monkeypatch.setenv('{0}_S3_BUCKET'.format(app_config.PROJECT_SLUG), 's3bucket.propublica.org')
    reload(app_config)
    assert app_config.S3_BUCKET == 's3bucket.propublica.org'


def test_get_env(monkeypatch):
    os.environ['{0}_TEST'.format(app_config.PROJECT_SLUG)] = 'test'
    reload(app_config)
    values = app_config.get_env()
    del os.environ['{0}_TEST'.format(app_config.PROJECT_SLUG)]
    assert values['TEST'] == 'test'


@pytest.mark.parametrize("value", ['TRUE', 'true', 'True', '1'])
def test_str_bool_truthy(value):
    assert app_config.str_bool(value)


@pytest.mark.parametrize("value", ['FALSE', 'false', 'False', '0'])
def test_str_bool_falsey(value):
    assert not app_config.str_bool(value)
