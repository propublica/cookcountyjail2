import os
import pytest

from imp import reload
from jailscraper import app_config


def clear_environ():
    keys = [k for k in os.environ.keys() if k.startswith(app_config.PROJECT_SLUG)]
    for k in keys:
        del(os.environ[k])


def test_disable_local_storage_with_string():
    clear_environ()
    os.environ['{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG)] = "fAlse"
    reload(app_config)
    assert not app_config.USE_LOCAL_STORAGE


def test_disable_local_storage_with_zero():
    clear_environ()
    os.environ['{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG)] = "0"
    reload(app_config)
    assert not app_config.USE_LOCAL_STORAGE


def test_enable_local_storage_with_string():
    clear_environ()
    os.environ['{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG)] = "tRue"
    reload(app_config)
    assert app_config.USE_LOCAL_STORAGE


def test_enable_local_storage_with_zero():
    clear_environ()
    os.environ['{0}_USE_LOCAL_STORAGE'.format(app_config.PROJECT_SLUG)] = "1"
    reload(app_config)
    assert app_config.USE_LOCAL_STORAGE


def test_default_local_storage():
    clear_environ()
    reload(app_config)
    assert app_config.USE_LOCAL_STORAGE


def test_disable_s3_storage_with_string():
    clear_environ()
    os.environ['{0}_USE_S3_STORAGE'.format(app_config.PROJECT_SLUG)] = "faLse"
    reload(app_config)
    assert not app_config.USE_S3_STORAGE


def test_disable_s3_storage_with_zero():
    clear_environ()
    os.environ['{0}_USE_S3_STORAGE'.format(app_config.PROJECT_SLUG)] = "0"
    reload(app_config)
    assert not app_config.USE_S3_STORAGE


def test_enable_s3_storage_with_string():
    clear_environ()
    os.environ['{0}_USE_S3_STORAGE'.format(app_config.PROJECT_SLUG)] = "True"
    reload(app_config)
    assert app_config.USE_S3_STORAGE


def test_enable_s3_storage_with_zero():
    clear_environ()
    os.environ['{0}_USE_S3_STORAGE'.format(app_config.PROJECT_SLUG)] = "1"
    reload(app_config)
    assert app_config.USE_S3_STORAGE


def test_default_s3_storage():
    clear_environ()
    reload(app_config)
    assert not app_config.USE_S3_STORAGE


def test_jail_number():
    clear_environ()
    os.environ['{0}_MAX_DEFAULT_JAIL_NUMBER'.format(app_config.PROJECT_SLUG)] = "100"
    reload(app_config)
    assert app_config.MAX_DEFAULT_JAIL_NUMBER == 100


def test_target():
    clear_environ()
    os.environ['{0}_TARGET'.format(app_config.PROJECT_SLUG)] = 'prod'
    reload(app_config)
    assert app_config.TARGET == 'prod'


def test_s3_bucket():
    clear_environ()
    os.environ['{0}_S3_BUCKET'.format(app_config.PROJECT_SLUG)] = 's3bucket.propublica.org'
    reload(app_config)
    assert app_config.S3_BUCKET == 's3bucket.propublica.org'


def test_get_env():
    clear_environ()
    os.environ['{0}_TEST'.format(app_config.PROJECT_SLUG)] = 'test'
    reload(app_config)
    values = app_config.get_env()
    assert values == {'TEST': 'test'}


@pytest.mark.parametrize("value", ['TRUE', 'true', 'True', '1'])
def test_str_bool_truthy(value):
    assert app_config.str_bool(value)


@pytest.mark.parametrize("value", ['FALSE', 'false', 'False', '0'])
def test_str_bool_falsey(value):
    assert not app_config.str_bool(value)
