from manager.validators import validation_date, validation_null_value, validate_stock
from manager.single_info import get_stock_country
import pandas as pd
import yfinance as yf

COUNTRY = "Poland"
STOCK = "AAPL"
START_DATE = pd.to_datetime("2020-01-01").date()
END_DATE = pd.to_datetime("2022-01-01").date()

DATAFRAME_INFLATION = pd.read_csv(f"data/Inflation/{COUNTRY}_inflation.csv", index_col=0, encoding="iso-8859-1")
DATAFRAME_CURRENCY = pd.read_csv(f"data/Currency_rate/{COUNTRY}_to_usd.csv", index_col=0)
DATAFRAME_STOCK = yf.download([STOCK], start=START_DATE, end=END_DATE, interval="1mo", progress=False)["Close"].to_frame().rename(columns={"Close": STOCK})


# Validation date
def test_validation_date():
    assert len(validation_date(DATAFRAME_STOCK, START_DATE, END_DATE)) == len(DATAFRAME_STOCK)


def test_validation_date_diffrence_in_date_old_input():
    start_date_old = pd.to_datetime("1900-01-01").date()
    assert len(validation_date(DATAFRAME_STOCK, start_date_old, END_DATE)) == len(DATAFRAME_STOCK)


def test_validation_date_diffrence_in_date_future_input():
    end_date_future = pd.to_datetime("2050-01-01").date()
    assert len(validation_date(DATAFRAME_STOCK, START_DATE, end_date_future)) == len(DATAFRAME_STOCK)


def test_validate_date_diffrence_bad_input():
    start_date_old = pd.to_datetime("1900-01-01").date()
    end_date_old = pd.to_datetime("1901-01-01").date()
    assert len(validation_date(DATAFRAME_STOCK, start_date_old, end_date_old)) == 0


def test_validate_date_cutted():
    start_date_cut = pd.to_datetime("2021-01-01").date()
    assert len(validation_date(DATAFRAME_STOCK, start_date_cut, END_DATE)) == 12


# Validation_null_value
def test_validation_null_value():
    assert validation_null_value(DATAFRAME_STOCK) is not None or validation_null_value(DATAFRAME_STOCK) is not str


# Validation stock
def test_validation_stock():
    result = get_stock_country("AAPL")
    assert result == "united_states"
    result = get_stock_country("INVALID")
    assert result == "No stock info"
