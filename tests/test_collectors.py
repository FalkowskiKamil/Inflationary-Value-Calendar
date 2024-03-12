from manager.collectors import api_stock_collector, api_list_of_available_collector,\
    api_databases_collector,  api_exchange_converter_collector, \
    api_inflation_converter_collector

from datetime import date
import pandas as pd
STOCK = "AAPL"
START_DATE = pd.to_datetime("2010-01-01").date()
END_DATE = pd.to_datetime("2015-01-01").date()


# Api exchange converter collector Part
def test_api_exchange_converter_collector_currency_exchange():
    result = api_exchange_converter_collector(converterCategory="currency_exchange", mainDataframeTitle="PLN", to_currency="JPY", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result.columns[0] == "JPY"
    assert len(result) == 61
    assert result.iloc[0].values[0] == 32.03160308665744


def test_api_exchange_converter_collector_currency_goods_currency_exchange():
    result = api_exchange_converter_collector(converterCategory="goods_currency_exchange", mainDataframeTitle="aluminum", to_currency="PLN", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result.columns[0] == "aluminum (Polish Złoty (PLN) per metric ton)"
    assert len(result) == 61
    assert result.iloc[0].values[0] == 6344.245279166658


def test_api_exchange_converter_collector_currency_stock_currency_exchange():
    result = api_exchange_converter_collector(converterCategory="stock_currency_exchange", mainDataframeTitle=STOCK, to_currency="PLN", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result.columns[0] == STOCK
    assert len(result) == 60
    assert result.iloc[0].values[0] == 19.51336165984469


def test_api_exchange_converter_collector_currency_invalid():
    result = api_exchange_converter_collector(converterCategory="Invalid", mainDataframeTitle="PLN", to_currency="USD", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result == "Invalid is invalid type of converter"


# Api inflation converter collector
def test_api_inflation_converter_collector_currency_rate_to_dollar_with_inflation():
    result = api_inflation_converter_collector(converterCategory="currency_rate_to_dollar_with_inflation", mainDataframeTitle="PLN", to_currency="USD", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result.columns[0] == "Polish Złoty (PLN) with inflation"
    assert len(result) == 61
    assert result.iloc[0].values[0] == 0.35151738337155436


def test_api_inflation_converter_collector_goods_value_with_inflation():
    result = api_inflation_converter_collector(converterCategory="goods_value_with_inflation", mainDataframeTitle="aluminum", to_currency="PLN", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result.columns[0] == "aluminum (Polish Złoty (PLN) per metric ton) with inflation"
    assert len(result) == 61
    assert result.iloc[0].values[0] == 6344.245279166658


def test_api_inflation_converter_collector_stock_value_with_inflation():
    result = api_inflation_converter_collector(converterCategory="stock_value_with_inflation", mainDataframeTitle=STOCK, to_currency="USD", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result.columns[0] == "AAPL with inflation"
    assert len(result) == 60
    assert result.iloc[0].values[0] == 6.859285831451416


def test_api_inflation_converter_collector_invalid():
    result = api_inflation_converter_collector(converterCategory="Invalid", mainDataframeTitle="PLN", to_currency="USD", start_dataframe_date=START_DATE, end_dataframe_date=END_DATE)
    assert result == "Invalid is invalid type of converter"


# Api databases collector
def test_api_databases_collector_inflation():
    result = api_databases_collector(databaseType="inflation", databaseKey="Poland", stockName="None", start_date=START_DATE, end_date=END_DATE)
    assert result.columns[0] == "Inflation in Poland indexed on 2010-01-01"
    assert len(result) == 61
    assert result.iloc[0].values[0] == 1.0


def test_api_databases_collector_goods():
    result = api_databases_collector(databaseType="goods", databaseKey="aluminum", stockName="None", start_date=START_DATE, end_date=END_DATE)
    assert result.columns[0] == "aluminum (dollar per metric ton) in USD"
    assert len(result.columns[0]) == 39
    assert result.iloc[0].values[0] == 2230.1125


def test_api_databases_collector_stock():
    result = api_databases_collector(databaseType="stock", databaseKey="None", stockName=STOCK, start_date=START_DATE, end_date=END_DATE)
    assert result.columns[0] == STOCK
    assert len(result) == 60
    assert result.iloc[0].values[0] == 6.859285831451416


def test_api_databases_collector_currency():
    result = api_databases_collector(databaseType="currency", databaseKey="PLN", stockName="None", start_date=START_DATE, end_date=END_DATE)
    assert result.columns[0] == "Polish Złoty (PLN)"
    assert len(result) == 61
    assert result.iloc[0].values[0] == 2.84480952380952


def test_api_databases_collector_invalid():
    result = api_databases_collector(databaseType="INVALID", databaseKey="INVALID", stockName="None", start_date=START_DATE, end_date=END_DATE)
    assert result == "INVALID is invalid type of database"


# Api stock collector
def test_api_stock_collector_stock_date():
    result = api_stock_collector("stock date", STOCK)
    assert result == f"1985-01-01, 2024-{date.today().strftime('%m')}-01"


def test_api_stock_collector_country():
    result = api_stock_collector("country", STOCK)
    assert result == "united_states"


def test_api_stock_collector_currency():
    result = api_stock_collector("currency", STOCK)
    assert result == "USD"


def test_api_stock_collector_long_name():
    result = api_stock_collector("long name", STOCK)
    assert result == "Apple Inc."


def test_api_stock_collector_last_value():
    result = api_stock_collector("last value", STOCK)
    assert int(result) > 0


def test_api_stock_collector_invalid():
    result = api_stock_collector("invalid", STOCK)
    assert result is None


# Api list of available collector
def test_api_list_of_available_collector_country():
    result = api_list_of_available_collector("country")
    assert len(result) == 43
    assert result[0] == "Australia"


def test_api_list_of_available_collector_goods():
    result = api_list_of_available_collector("goods")
    assert len(result) == 30
    assert result[0] == "Aluminum"


def test_api_list_of_available_collector_currency():
    result = api_list_of_available_collector("currency")
    assert len(result) == 33
    assert result[0] == "Argentine Peso (ARS)"


def test_api_list_of_available_collector_invalid():
    result = api_list_of_available_collector("Invalid")
    assert result is None
