

TEST_INMATES_CSV = [
    {
        'Age_At_Booking': 21,
        'Bail_Amount': '50,000.00',
        'Booking_Id': '2015-0904292',
        'Charges': """720 ILCS 5/11-9(a)(2)
PUBLIC INDECENCY/LEWD EXPOSURE""",
        'Court_Date': '2017-07-20',
        'Court_Location': """Criminal Courts Building
Criminal Courts Building

,""",
        'Gender': 'Male',
        'Height': '509',
        'Housing_Location': 'DIV9-3B-3105-1',
        'Inmate_Hash': '7b7d440062f7cf7b3bc15a6c0fd543f4d84fd2e74d05969401085ce5c8d3e03b',
        'Race': 'BK',
        'Weight': '160',
    },
    # Just a random inmate
    {
        'Age_At_Booking': 21,
        'Bail_Amount': '50,000.00',
        'Booking_Id': '2017-0608010',
        'Charges': """720 ILCS 5/24-1.6(a)(3)(a)(5)
AGG UUW/LOADED PISTOL, REVOLVER, HANDGUN-NO CCL""",
        'Court_Date': '2017-06-28',
        'Court_Location': """Markham
Markham

,""",
        'Gender': 'Male',
        'Height': '507',
        'Housing_Location': 'DIV2-D1-D-32',
        'Inmate_Hash': 'af4da0bc3ecf5fe9568b902fbcec6588282c7c3b5377cfba94a44e3ce0ea3978',
        'Race': 'BK',
        'Weight': '165',
    },
    {
        'Age_At_Booking': 27,
        'Bail_Amount': '*NO BOND*',
        'Booking_Id': '2017-0612061',
        'Charges': '',
        'Court_Date': '',
        'Court_Location': '',
        'Gender': 'Male',
        'Height': '510',
        'Housing_Location': '',
        'Inmate_Hash': 'ec407ab41d1d1fc319113516ce4f871a59a0b6f4c52a283507bf463d3fc55fdd',
        'Race': 'BK',
        'Weight': '185',
    },
]


def to_lower(inmate):
    return dict([(k.lower(), v) for k, v in inmate.items()])


TEST_INMATES = map(to_lower, TEST_INMATES_CSV)
