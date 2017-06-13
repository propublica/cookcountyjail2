import pytest

from jailscraper.models import InmatePage


def get_inmate(id):
    with open('tests/sample_pages/{0}.html'.format(id)) as f:
        body = f.read()
    return InmatePage(body)

# @TODO is there a way to do this more elegantly with fixtures?
testdata = (
    # An old inmate: Especially important is to make sure hash is correct
    (get_inmate('2015-0904292'), {
        'age_at_booking': 21,
        'bail_amount': '50,000.00',
        'booking_id': '2015-0904292',
        'charges': """720 ILCS 5/11-9(a)(2)
PUBLIC INDECENCY/LEWD EXPOSURE""",
        'court_date': '2017-07-20',
        'court_location': """Criminal Courts Building
Criminal Courts Building

,""",
        'gender': 'Male',
        'height': '509',
        'housing_location': 'DIV9-3B-3105-1',
        'inmate_hash': '7b7d440062f7cf7b3bc15a6c0fd543f4d84fd2e74d05969401085ce5c8d3e03b',
        'race': 'BK',
        'weight': '160',
    }),
    # Just a random inmate
    (get_inmate('2017-0608010'), {
        'age_at_booking': 21,
        'bail_amount': '50,000.00',
        'booking_id': '2017-0608010',
        'charges': """720 ILCS 5/24-1.6(a)(3)(a)(5)
AGG UUW/LOADED PISTOL, REVOLVER, HANDGUN-NO CCL""",
        'court_date': '2017-06-28',
        'court_location': """Markham
Markham

,""",
        'gender': 'Male',
        'height': '507',
        'housing_location': 'DIV2-D1-D-32',
        'inmate_hash': 'af4da0bc3ecf5fe9568b902fbcec6588282c7c3b5377cfba94a44e3ce0ea3978',
        'race': 'BK',
        'weight': '165',
    }),
    (get_inmate('2017-0612061'), {
        'age_at_booking': 27,
        'bail_amount': '*NO BOND*',
        'booking_id': '2017-0612061',
        'charges': '',
        'court_date': '',
        'court_location': '',
        'gender': 'Male',
        'height': '510',
        'housing_location': '',
        'inmate_hash': 'ec407ab41d1d1fc319113516ce4f871a59a0b6f4c52a283507bf463d3fc55fdd',
        'race': 'BK',
        'weight': '185',
    }),
)


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
