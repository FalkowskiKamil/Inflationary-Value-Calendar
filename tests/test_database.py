from manager.database import get_database_inflation,\
    get_database_stock,\
    get_database_prices,\
    get_database_currency_rate_to_dollar
import pandas as pd

COUNTRY = "Poland"
GOODS = "bananas"
STOCK = "AAPL"
START_DATE = pd.to_datetime("2010-01-01").date()
END_DATE = pd.to_datetime("2015-01-01").date()


# Country inflation
def test_database_inflation_head():
    assert get_database_inflation(COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[144.86186], [145.1157], [148.71653]]


def test_database_inflation_tail():
    assert get_database_inflation(COUNTRY, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[138.45289], [140.17262], [137.98035]]


def test_database_inflation_length():
    assert len(get_database_inflation(COUNTRY, START_DATE, END_DATE)) == 61


# Prices
def test_database_prices_head():
    print(get_database_prices(GOODS, START_DATE, END_DATE)[:3].values.tolist())
    assert get_database_prices(GOODS, START_DATE, END_DATE)[:3].values.tolist() == [[782.68876611418], [790.745856353591], [842.541436464088]]


def test_database_prices_length():
    assert len(get_database_prices(GOODS, START_DATE, END_DATE)) == 61


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
