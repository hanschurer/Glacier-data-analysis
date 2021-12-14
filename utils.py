import math


def haversine_distance(lat1, lon1, lat2, lon2):
    for i in [lat1, lat2]:
        check_lat_range(i)
    for j in [lon1, lon2]:
        check_lon_range(j)

    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    result = 2*R*math.asin((pow(math.sin((lat2-lat1)/2), 2)+math.cos(lat1)
                           * math.cos(lat2)*pow(math.sin((lon2-lon1)/2), 2))**0.5)
    return result


def check_ID(id):
    if isinstance(id, str):
        if id.isdigit():
            if len(id) != 5:
                raise ValueError(
                    "'The unique ID should comprised of exactly 5 digits.'")
        else:
            raise ValueError("'The unique ID should be digits.'")
    else:
        raise TypeError("'The unique ID should be a String'")


def check_single_year_validate(year):
    try:
        year = int(year)
    except:
        raise TypeError('The year must be convertible to int')

    if isinstance(year, int):
        if year < 2022:
            pass
        else:
            raise ValueError('Year must be not in the furture')
    else:
        raise ValueError('Year must be an integer number.')


def check_lon_range(value):
    try:
        value = float(value)
    except:
        raise TypeError('The longtitude must be convertible to float')

    if value < -180 or value > 180:
        raise ValueError(
            "The longitude is not in range, should be between -180 and 180")


def check_lat_range(value):
    try:
        value = float(value)
    except:
        raise TypeError('The latitude must be convertible to float')

    if value < -90 or value > 90:
        raise ValueError(
            "The latitude is not in range, should be between -90 and 90")


def check_political_unit(unit):
    if isinstance(unit, str):
        if len(unit) == 2:
            if unit == '99':
                pass
            elif unit.isupper():
                pass
            else:
                raise ValueError(
                    "The Plolitical unit should be only of capital letters or the special value ”99”")
        else:
            raise ValueError(
                "The Plolitical unit should be a string of length 2.")
    else:
        raise ValueError("'The plolitical unit should be a String'")


def check_mass_balance_value(value):
    try:
        value = float(value)
    except:
        raise TypeError('The mass balance must be a number')

    if not isinstance(value, int):
        if not isinstance(value, float):
            raise ValueError('The mass balance value should be a number')


def check_code_pattern(value):
    scope = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '?']

    if isinstance(value, str):
        if len(value) == 3:
            for i in value:
                if i in scope:
                    pass
                else:
                    raise ValueError(
                        'The code pattern should be 3 digits or "?"')
    elif isinstance(value, int):
        if value < 999 and value > 100:
            pass
        else:
            raise ValueError('The code pattern should be 3 digits')
    else:
        raise TypeError('The code pattern should be neither string or integer')


def check_code(code):
    try:
        code = int(code)
    except:
        raise TypeError('The code must be convertible to int')
    if code < 999 and code > 100:
        pass
    else:
        raise ValueError('The code must be 3 digits')
