from manager.utils import concat_dataframe_with_inflation, concat_dataframe_with_exchange_rate, \
    convert_currency_to_usd, convert_currency_to_other_currency, \
    convert_form_date_to_pandas_date_type, finding_exchanging_rate, \
    indexing_on_start_date, unify_dataframes_date
from manager.database import get_database_currency_rate_to_dollar
import pandas as pd
import yfinance as yf

COUNTRY = "Poland"
COUNTRY_2 = "Japan"
STOCK = "AAPL"
START_DATE = pd.to_datetime("2020-01-01").date()
END_DATE = pd.to_datetime("2022-01-01").date()
FIRST_CURRENCY = "JPY"
SECOND_CURRENCY = "PLN"


DATAFRAME_INFLATION = pd.read_csv(f"data/Inflation/{COUNTRY}_inflation.csv", index_col=0, encoding="iso-8859-1")
DATAFRAME_CURRENCY = pd.read_csv(f"data/Currency_rate/{COUNTRY}_to_usd.csv", index_col=0)
DATAFRAME_CURRENCY_2 = pd.read_csv(f"data/Currency_rate/{COUNTRY_2}_to_usd.csv", index_col=0)
DATAFRAME_STOCK = yf.download([STOCK], start=START_DATE, end=END_DATE, interval="1mo", progress=False)["Close"].to_frame().rename(columns={"Close": STOCK})
DATAFRAME_RATE = get_database_currency_rate_to_dollar(COUNTRY, START_DATE, END_DATE)


# Concat dataframe with inflation
def test_concat_dataframe_with_inflation():
    dataframe = concat_dataframe_with_inflation(DATAFRAME_INFLATION, DATAFRAME_CURRENCY)
    assert dataframe.head(1).values.tolist() == [[0.0158841904571429]]


# Concat dataframe with exchange rate
def test_concat_dataframe_with_exchange_rate():
    dataframe = concat_dataframe_with_exchange_rate(DATAFRAME_STOCK, DATAFRAME_RATE)
    assert dataframe.head(1).values.tolist() == [[296.3504515678075]]


# Convert currency to USD
def test_convert_currency_to_usd():
    dataframe = convert_currency_to_usd(SECOND_CURRENCY, START_DATE, END_DATE)
    print(dataframe.iloc[0])
    print(dataframe.iloc[-1])
    assert dataframe.head(1).values.tolist() == [[0.2611013481911352]]


# Convert currency to other currency
def test_convert_currency_to_other_currency():
    dataframe = convert_currency_to_other_currency(DATAFRAME_CURRENCY, DATAFRAME_CURRENCY_2)
    assert dataframe.head(1).values.tolist() == [900895.8077499999]


# Convert form date to pandas date type
def test_form_date_to_pandas_date_type():
    start_date, end_date = convert_form_date_to_pandas_date_type(2000, 1, 2010, 1)
    assert start_date == pd.to_datetime("2000-01-01").date()
    assert end_date == pd.to_datetime("2010-01-01").date()


# Finding exchanging rate
def test_finding_exchanging_rate():
    dataframe = finding_exchanging_rate(FIRST_CURRENCY, SECOND_CURRENCY, START_DATE, END_DATE)
    assert dataframe.head(1).values.tolist() == [[0.03502980510365165]]


# Indexing on start date
def test_indexing_on_start_date():
    dataframe = DATAFRAME_STOCK[START_DATE: END_DATE]
    dataframe = indexing_on_start_date(dataframe)
    assert dataframe.head(1).values == [1.0]


# Unify dataframes date()
def test_unify_dataframes_date():
    start_date, end_date = unify_dataframes_date(DATAFRAME_INFLATION, DATAFRAME_CURRENCY)
    assert start_date == "1993-01-01"
    assert end_date == "2023-12-01"
