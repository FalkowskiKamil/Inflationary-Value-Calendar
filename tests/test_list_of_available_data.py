from manager.list_of_available_data import get_list_of_available_currency_by_country_data, \
    get_list_of_available_goods_prices_data, \
    get_list_of_available_inflation_country_data




# Country part
def test_list_of_country_head():
    assert get_list_of_available_inflation_country_data()[:3] == ["australia", "austria", "belgium"]


def test_list_of_country_tail():
    assert get_list_of_available_inflation_country_data()[-3:] == ["turkey", "united_kingdom", "united_states"]


def test_list_of_country_length():
    assert len(get_list_of_available_inflation_country_data()) == 43


# Goods part
def test_list_of_goods_head():
    assert get_list_of_available_goods_prices_data()[:3] == ["aluminum", "bananas", "barley"]


def test_list_of_goods_tail():
    assert get_list_of_available_goods_prices_data()[-3:] == ["uranium", "wheat", "wti"]


def test_list_of_goods_length():
    assert len(get_list_of_available_goods_prices_data()) == 24


# Currency part
def test_list_of_currency_head():
    assert get_list_of_available_currency_by_country_data()[:3] == ["argentina", "australia", "austria"]


def test_list_of_currency_tail():
    assert get_list_of_available_currency_by_country_data()[-3:] == ["switzerland", "turkey", "united_kingdom"]


def test_list_of_currency_length():
    assert len(get_list_of_available_currency_by_country_data()) == 51
