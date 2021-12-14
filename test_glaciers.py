from glaciers import Glacier, GlacierCollection
import utils
from pathlib import Path
from pytest import raises
import pytest

# negetive test

def test_check_ID():
    with raises(ValueError) as exception:
        utils.check_ID('122223')
    with raises(ValueError) as exception:
        utils.check_ID('fdsak')
    with raises(TypeError) as exception:
        utils.check_ID(True)


def test_check_lat_range():
    with raises(TypeError) as exception:
        utils.check_lon_range([False])
    with raises(ValueError) as exception:
        utils.check_lat_range(100)


def test_check_lon_range():
    with raises(TypeError) as exception:
        utils.check_lon_range({})
    with raises(ValueError) as exception:
        utils.check_lon_range(289)


def test_check_political_unit():
    with raises(ValueError) as exception:
        utils.check_political_unit('AAA1')
    with raises(ValueError) as exception:
        utils.check_political_unit('AAA1')
    with raises(ValueError) as exception:
        utils.check_political_unit('AAA1')


def test_check_single_year_validate():
    with raises(TypeError) as exception:
        utils.check_single_year_validate((True, 4))
    with raises(ValueError) as exception:
        utils.check_single_year_validate(2893.222)
    with raises(ValueError) as exception:
        utils.check_single_year_validate(2893)


def test_check_mass_balance_value():
    with raises(TypeError) as exception:
        utils.check_mass_balance_value([{'none'}])


def test_check_code_pattern():
    with raises(ValueError) as exception:
        utils.check_code_pattern('3FA')
        utils.check_code_pattern(9999)
    with raises(TypeError) as exception:
        utils.check_mass_balance_value([{'none'}])


@pytest.fixture()
def Collection() -> GlacierCollection:
    file_path = Path("test-A.csv")
    mass_data_path = Path('test-B.csv')
    Collection = GlacierCollection(file_path)
    Collection.read_mass_balance_data(mass_data_path)
    return Collection


def test_add_mass_balance_measurement(Collection):
    Collection.read_mass_balance_data(Path('test-B.csv'))
    assert Collection.collection[0].mass[2015] == [-793.0, False]
    assert Collection.collection[0].mass[2018] == [-15772.0]


def test_filter_by_code(Collection):
    number = Collection.filter_by_code('538')
    sign = Collection.filter_by_code('5?8')
    assert number == ['AZUFRE', 'FRIAS', 'PILOTO ESTE', 'URUMQI GLACIER NO. 1 E-BRANCH',
                      'URUMQI GLACIER NO. 1 W-BRANCH', 'XIAO DONGKZMADI', 'CORNELIUSSENBREEN']
    assert sign == ['AZUFRE', 'CANON HISPANO', 'FRIAS', 'PILOTO ESTE', 'TURTMANN', 'PARLUNG NO. 94', 'URUMQI GLACIER NO. 1 E-BRANCH',
                    'URUMQI GLACIER NO. 1 W-BRANCH', 'XIAO DONGKZMADI', 'GLJUFURARJOKULL', 'CORNELIUSSENBREEN', 'STORSTEINSFJELLBREEN', 'SYDBREEN']


def test_sort_by_latest_mass_balance(Collection):
    reverse = Collection.sort_by_latest_mass_balance(reverse=True, n=3)
    anti_reverse = Collection.sort_by_latest_mass_balance(reverse=False)

    reverse_list = []
    anti_reverse_list = []

    for i in reverse:
        reverse_list.append(i.name)
    for i in anti_reverse:
        anti_reverse_list.append(i.name)

    print(anti_reverse_list)
    print(reverse_list)

    assert reverse_list == ['ARTESONRAJU','TUNSBERGDALSBREEN', 'PARLUNG NO. 94']
    assert anti_reverse_list == ['STORSTEINSFJELLBREEN', 'CAINHAVARRE', 'BLAAISEN', 'REMBESDALSKAAKA', 'CHHOTA SHIGRI']
