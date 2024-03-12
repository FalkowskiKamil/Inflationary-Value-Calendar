from manager.list_of_available_data import get_list_of_available_country_with_currency_data, \
    get_list_of_available_currency_data, \
    get_list_of_available_goods_prices_data, \
    get_list_of_available_inflation_country_data


# Country part
def test_list_of_country_head():
    assert get_list_of_available_inflation_country_data()[:3] == ["Australia", "Austria", "Belgium"]


def test_list_of_country_tail():
    assert get_list_of_available_inflation_country_data()[-3:] == ["Turkey", "United kingdom", "United states"]


def test_list_of_country_length():
    assert len(get_list_of_available_inflation_country_data()) == 43


def test_get_list_of_available_currency_data_length():
    assert len(get_list_of_available_currency_data()) == 48


# Goods part
def test_list_of_goods_head():
    assert get_list_of_available_goods_prices_data()[:3] == ["Aluminum", "Bananas", "Barley"]


def test_list_of_goods_tail():
    assert get_list_of_available_goods_prices_data()[-3:] == ["Wheat", "Wool fine", "Wti"]


def test_list_of_goods_length():
    assert len(get_list_of_available_goods_prices_data()) == 30


# Currency part
def test_list_of_currency_head():
    assert get_list_of_available_country_with_currency_data()[:3] == ["Argentina", "Australia", "Austria"]


def test_list_of_currency_tail():
    assert get_list_of_available_country_with_currency_data()[-3:] == ["Switzerland", "Turkey", "United_kingdom"]


def test_list_of_currency_length():
    assert len(get_list_of_available_country_with_currency_data()) == 51


# Inflation part
def test_list_of_inflation_country_head():
    assert get_list_of_available_inflation_country_data()[:3] == ["Australia", "Austria", "Belgium"]


def test_list_of_inflation_country_tail():
    assert get_list_of_available_inflation_country_data()[-3:] == ["Turkey", "United kingdom", "United states"]


def test_list_of_inflation_country_length():
    assert len(get_list_of_available_inflation_country_data()) == 43

