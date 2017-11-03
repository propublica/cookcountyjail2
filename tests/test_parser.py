import pytest

from jailscraper.models import InmatePage
from tests import TEST_INMATES


def get_inmate(id):
    with open('tests/sample_pages/{0}.html'.format(id)) as f:
        body = f.read()
    return InmatePage(body)


expected = (
    get_inmate('2015-0904292'),
    get_inmate('2017-0608010'),
    get_inmate('2017-0612061'),
)


# @TODO is there a way to do this more elegantly with fixtures?
testdata = list(zip(expected, TEST_INMATES))


@pytest.mark.parametrize("inmate,expected", testdata)
def test_bail_amount(inmate, expected):
    assert inmate.bail_amount == expected['bail_amount']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_age_at_booking(inmate, expected):
    assert inmate.age_at_booking == expected['age_at_booking']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_housing_location(inmate, expected):
    assert inmate.housing_location == expected['housing_location']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_race(inmate, expected):
    assert inmate.race == expected['race']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_gender(inmate, expected):
    assert inmate.gender == expected['gender']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_height(inmate, expected):
    assert inmate.height == expected['height']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_weight(inmate, expected):
    assert inmate.weight == expected['weight']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_booking_id(inmate, expected):
    assert inmate.booking_id == expected['booking_id']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_court_date(inmate, expected):
    assert inmate.court_date == expected['court_date']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_charges(inmate, expected):
    assert inmate.charges == expected['charges']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_court_location(inmate, expected):
    assert inmate.court_location == expected['court_location']


@pytest.mark.parametrize("inmate,expected", testdata)
def test_inmate_hash(inmate, expected):
    assert inmate.inmate_hash == expected['inmate_hash']
