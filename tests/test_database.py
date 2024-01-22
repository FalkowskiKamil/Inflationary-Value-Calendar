from manager.database import get_database_inflation,\
    get_database_stock,\
    get_database_prices,\
    get_database_currency_rate_to_dollar,\
    get_database_currency_index_to_dollar

COUNTRY = "Poland"
GOODS = "bananas"
STOCK1 = "AAPL"
STOCK2 = "GOOG"
START_DATE = "2010-01-01"
END_DATE = "2015-01-01"


# Country inflation
def test_database_inflation_head():
    assert get_database_inflation(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[144.86186], [145.1157], [148.71653]]


def test_database_inflation_tail_without_date():
    assert get_database_inflation(COUNTRY).iloc[-3:].values.tolist() == [[157.52997], [151.56092], [154.39214]]


def test_database_inflation_length():
    assert len(get_database_inflation(COUNTRY, START_DATE, END_DATE)) == 60


# Prices
def test_database_prices_head():
    assert get_database_prices(GOODS, START_DATE, END_DATE)[:3].values.tolist() == [[132.7266], [134.0929], [142.87628]]


def test_database_prices_tail_without_date():
    assert get_database_prices(GOODS)[-3:].values.tolist() == [[264.67246], [265.78781], [267.01469]]


def test_database_prices_length():
    assert len(get_database_prices(GOODS, START_DATE, END_DATE)) == 61


# Stock
def test_database_stock_single_head():
    assert get_database_stock([STOCK1], START_DATE, END_DATE).iloc[:3].values.tolist() == [[6.859285831451416], [7.307857036590576], [8.39285659790039]]


def test_database_stock_single_column_name():
    assert get_database_stock([STOCK1], START_DATE, END_DATE).columns[0] == STOCK1


def test_database_stock_multi_tail():
    assert get_database_stock([STOCK1, STOCK2], START_DATE, END_DATE).iloc[-3:].values.tolist() == [[27.0, 27.87746238708496], [29.732500076293945, 27.017324447631836], [27.594999313354492, 26.247936248779297]]


def test_database_stock_single_length():
    assert len(get_database_stock([STOCK1], START_DATE, END_DATE)) == 60


# Currency rate to dollar
def test_database_currency_rate_head():
    assert get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[2.84480952380952], [2.93005], [2.86360869565217]]


def test_database_currency_rate_tail():
    assert get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[3.31692173913043], [3.377455], [3.42701739130435]]


def test_database_currency_rate_column_name():
    assert get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE).columns[0] == "Polish Złoty (PLN)"


def test_database_currency_rate_length():
    assert len(get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE)) == 60


# Currency index to dollar
def test_database_currency_index_head():
    assert get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[711202.38095], [732512.5], [715902.17391]]


def test_database_currency_index_tail():
    assert get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[829230.43478], [844363.75], [856754.34783]]


def test_database_currency_index_column_name():
    assert get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE).columns[0] == "Polish Złoty (PLN)"


def test_database_currency_index_length():
    assert len(get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE)) == 60
