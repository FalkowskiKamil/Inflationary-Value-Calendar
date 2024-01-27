from manager.database import get_database_inflation,\
    get_database_stock,\
    get_database_prices,\
    get_database_currency_rate_to_dollar,\
    get_database_currency_index_to_dollar
import pandas as pd

COUNTRY = "Poland"
GOODS = "bananas"
STOCK = "AAPL"
START_DATE = pd.to_datetime("2010-01-01").date()
END_DATE = pd.to_datetime("2015-01-01").date()


# Country inflation
def test_database_inflation_head():
    assert get_database_inflation(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[144.86186], [145.1157], [148.71653]]


def test_database_inflation_tail_without_date():
    assert get_database_inflation(COUNTRY).iloc[-3:].values.tolist() == [[154.39214], [159.69771], [162.66146]]


def test_database_inflation_length():
    assert len(get_database_inflation(COUNTRY, START_DATE, END_DATE)) == 61


def test_database_inflation_no_date():
    assert len(get_database_inflation(COUNTRY)) == 372


# Prices
def test_database_prices_head():
    assert get_database_prices(GOODS, START_DATE, END_DATE)[:3].values.tolist() == [[132.7266], [134.0929], [142.87628]]


def test_database_prices_tail_without_date():
    assert get_database_prices(GOODS)[-3:].values.tolist() == [[265.78781], [267.01469], [262.96901]]


def test_database_prices_length():
    assert len(get_database_prices(GOODS, START_DATE, END_DATE)) == 61


def test_database_prices_no_date():
    assert len(get_database_prices(GOODS)) == 407


# Stock
def test_database_stock_head():
    assert get_database_stock(STOCK, START_DATE, END_DATE).iloc[:3].values.tolist() == [[6.859285831451416], [7.307857036590576], [8.39285659790039]]


def test_database_stock_tail():
    assert get_database_stock(STOCK, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[27.0], [29.732500076293945], [27.594999313354492]]


def test_database_stock_length():
    assert len(get_database_stock(STOCK, START_DATE, END_DATE)) == 60


def test_database_stock_column_name():
    assert get_database_stock(STOCK, START_DATE, END_DATE).columns[0] == STOCK


# Currency rate to dollar
def test_database_currency_rate_head():
    assert get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[2.84480952380952], [2.93005], [2.86360869565217]]


def test_database_currency_rate_tail():
    assert get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[3.377455], [3.42701739130435], [3.67282272727273]]


def test_database_currency_rate_length():
    assert len(get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE)) == 61


def test_database_currency_rate_column_name():
    assert get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE).columns[0] == "Polish Złoty (PLN)"


def test_database_currency_rate_no_date():
    assert len(get_database_currency_rate_to_dollar(COUNTRY)) == 768


# Currency index to dollar
def test_database_currency_index_head():
    assert get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[711202.38095], [732512.5], [715902.17391]]


def test_database_currency_index_tail():
    assert get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[844363.75], [856754.34783], [918205.68182]]


def test_database_currency_index_length():
    assert len(get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE)) == 61


def test_database_currency_index_column_name():
    assert get_database_currency_index_to_dollar(COUNTRY, START_DATE, END_DATE).columns[0] == "Polish Złoty (PLN)"


def test_database_currency_index_no_date():
    assert len(get_database_currency_index_to_dollar(COUNTRY)) == 768
