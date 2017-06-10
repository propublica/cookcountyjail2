import pytest

from jailscraper.models import InmatePage

def get_inmate(id):
    with open('tests/sample_pages/{0}.html'.format(id)) as f:
        body = f.read()
    return InmatePage(body)

inmate = get_inmate('2017-0608010')

def test_bail_amount():
    assert inmate.bail_amount == '50,000.00'

def test_age_at_booking():
    assert inmate.age_at_booking == 21

def test_housing_location():
    assert inmate.housing_location == 'DIV2-D1-D-32'

def test_race():
    assert inmate.race == 'BK'

def test_gender():
    assert inmate.gender == 'Male'

def test_height():
    assert inmate.height == '507'

def test_weight():
    assert inmate.weight == '165'

def test_booking_id():
    assert inmate.booking_id == '2017-0608010'

def test_court_date():
    assert inmate.court_date == '2017-06-28'

def test_charges():
    assert inmate.charges == """720 ILCS 5/24-1.6(a)(3)(a)(5)
AGG UUW/LOADED PISTOL, REVOLVER, HANDGUN-NO CCL"""

def test_court_location():
    assert inmate.court_location == """Markham
Markham

,"""
