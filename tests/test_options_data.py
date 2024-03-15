from manager.options_data import get_options_country_with_currency_data, \
    get_options_currency_data, \
    get_options_goods_prices_data, \
    get_options_inflation_country_data


# Currency part
def test_options_country_with_currency_data_head():
    assert get_options_country_with_currency_data()[:3] == ["Argentina", "Australia", "Austria"]


def test_options_country_with_currency_data_tail():
    assert get_options_country_with_currency_data()[-3:] == ["Switzerland", "Turkey", "United_kingdom"]


def test_options_country_with_currency_data_length():
    assert len(get_options_country_with_currency_data()) == 51


# Country part
def test_get_options_currency_data_head():
    assert list(get_options_currency_data().values())[:3] == ['Argentine Peso (ARS)', 'Australian Dollar (AUD)', 'Euro (EUR)']


def test_get_options_currency_data_tail():
    assert list(get_options_currency_data().values())[-3:] == ['British Pound (GBP)', 'United States Dollar (USD)', 'Special Drawing Rights (SDR)']


def test_get_options_currency_data_length():
    assert len(get_options_currency_data()) == 48


# Goods part
def test_options_goods_prices_data_head():
    assert get_options_goods_prices_data()[:3] == ["Aluminum", "Bananas", "Barley"]


def test_options_goods_prices_data_tail():
    assert get_options_goods_prices_data()[-3:] == ["Wheat", "Wool fine", "Wti"]


def test_options_goods_prices_data_length():
    assert len(get_options_goods_prices_data()) == 30


# Inflation part
def test_options_inflation_country_data_head():
    assert get_options_inflation_country_data()[:3] == ["Australia", "Austria", "Belgium"]


def test_ooptions_inflation_country_data_tail():
    assert get_options_inflation_country_data()[-3:] == ["Turkey", "United kingdom", "United states"]


def test_options_inflation_country_data_length():
    assert len(get_options_inflation_country_data()) == 43

