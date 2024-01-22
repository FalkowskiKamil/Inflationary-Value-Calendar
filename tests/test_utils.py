from manager.utils import concat_database_with_inflation,\
    convert_index_to_DatetimeIndex,\
    convert_country_to_currency,\
    plotting_database
import pandas as pd
import yfinance as yf
COUNTRY = "Poland"
STOCK1 = "AAPL"
STOCK2 = "GOOG"
START_DATE = "2020-01-01"
END_DATE = "2022-01-01"

DATAFRAME_INFLATION = pd.read_csv(f"data/Inflation/{COUNTRY}_inflation.csv", index_col=0, encoding="iso-8859-1")
DATAFRAME_CURRENCY = pd.read_csv(f"data/Currency_rate/{COUNTRY}_to_usd.csv", index_col=0)
DATAFRAME_STOCK = yf.download([STOCK1, STOCK2], start=START_DATE, end=END_DATE, interval="1mo", progress=False)['Close']

# Concat
def test_concat_database_with_inflation():
    dataframe = concat_database_with_inflation(DATAFRAME_INFLATION, DATAFRAME_CURRENCY)
    assert dataframe.head(1).values.tolist() == [[100.0, 1.58841904571429, 1.58841904571429]]


# Convert index to DatetimeIndex
def test_convert_index_type_to_DatetimeIndex():
    assert DATAFRAME_CURRENCY.index.dtype == "object"
    dataframe = convert_index_to_DatetimeIndex(DATAFRAME_CURRENCY)
    assert dataframe.index.dtype == "datetime64[ns]"


# Convert country to currency
def test_convert_country_to_currency():
    assert convert_country_to_currency(DATAFRAME_CURRENCY).columns[0] == "Polish Złoty (PLN)"

# plotting
"""
def test_plotting_one_column():
    plotting_database(DATAFRAME_STOCK)


def test_plotting_multiply_value():
    database = concat_database_with_inflation(DATAFRAME_INFLATION, DATAFRAME_STOCK)
    plotting_database(database)
"""
