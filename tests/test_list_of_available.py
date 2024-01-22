from manager.list_of_available import get_list_of_available_stock_from_file, \
    get_list_of_available_inflation_country_from_file, \
    get_list_of_available_goods_prices_from_file, \
    get_list_of_available_currency_by_country_from_file


# Stock part
def test_list_of_stock_head():
    assert get_list_of_available_stock_from_file().iloc[:3].index.to_list() == ['06N.WA', '11B.WA', '1AT.WA']


def test_list_of_stock_tail():
    assert get_list_of_available_stock_from_file().iloc[-3:].index.to_list() == ['ZWS', 'ZYME', 'ZYXI']


def test_list_of_stock_length():
    assert len(get_list_of_available_stock_from_file()) == 7474


def test_list_of_stock_value_from_symbol():
    assert get_list_of_available_stock_from_file().loc["ALE.WA"]["Name"] == "ALLEGRO"


# Country part
def test_list_of_country_head():
    assert get_list_of_available_inflation_country_from_file()[:3] == ["australia", "austria", "belgium"]


def test_list_of_country_tail():
    assert get_list_of_available_inflation_country_from_file()[-3:] == ["turkey", "united", "usa"]


def test_list_of_country_length():
    assert len(get_list_of_available_inflation_country_from_file()) == 43


# Goods part
def test_list_of_goods_head():
    assert get_list_of_available_goods_prices_from_file()[:3] == ["aluminum", "bananas", "barley"]


def test_list_of_goods_tail():
    assert get_list_of_available_goods_prices_from_file()[-3:] == ['uranium', 'wheat', 'wti']


def test_list_of_goods_length():
    assert len(get_list_of_available_goods_prices_from_file()) == 24


# Currency part
def test_list_of_currency_head():
    assert get_list_of_available_currency_by_country_from_file()[:3] == ["argentina", "australia", "austria"]


def test_list_of_currency_tail():
    assert get_list_of_available_currency_by_country_from_file()[-3:] == ['switzerland', 'turkey', 'uk']


def test_list_of_currency_length():
    assert len(get_list_of_available_currency_by_country_from_file()) == 52
