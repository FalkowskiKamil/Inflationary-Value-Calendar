from manager.utils import concat_database_with_inflation, \
    convert_country_to_currency, \
    convert_usd_to_other_currency, \
    validation_date, \
    validation_null_value
import pandas as pd
import yfinance as yf

COUNTRY = "Poland"
STOCK = "AAPL"
START_DATE = pd.to_datetime("2020-01-01").date()
END_DATE = pd.to_datetime("2022-01-01").date()

DATAFRAME_INFLATION = pd.read_csv(f"data/Inflation/{COUNTRY}_inflation.csv", index_col=0, encoding="iso-8859-1")
DATAFRAME_CURRENCY = pd.read_csv(f"data/Currency_rate/{COUNTRY}_to_usd.csv", index_col=0)
DATAFRAME_STOCK = yf.download([STOCK], start=START_DATE, end=END_DATE, interval="1mo", progress=False)["Close"].to_frame().rename(columns={"Close": STOCK})


# Concat
def test_concat_database_with_inflation():
    dataframe = concat_database_with_inflation(DATAFRAME_INFLATION, DATAFRAME_CURRENCY)
    assert dataframe.head(1).values.tolist() == [[100.0, 1.58841904571429, 0.0158841904571429]]


# Convert country to currency
def test_convert_country_to_currency():
    assert convert_country_to_currency(DATAFRAME_CURRENCY).columns[0] == "Polish Złoty (PLN)"


def test_convert_country_to_currency_length():
    assert len(convert_country_to_currency(DATAFRAME_CURRENCY)) == len(DATAFRAME_CURRENCY)


# Convert USD to other currency
def test_convert_usd_to_other_currency_head():
    assert convert_usd_to_other_currency(DATAFRAME_STOCK, COUNTRY, START_DATE, END_DATE).iloc[-3:].values.tolist() == [[593.2151454184398], [672.6785946916756], [725.286239002791]]


def test_convert_usd_to_other_currency_tail():
    assert convert_usd_to_other_currency(DATAFRAME_STOCK, COUNTRY, START_DATE, END_DATE).iloc[:3].values.tolist() == [[296.3504515678075], [267.9724017402649], [255.1554461610103]]


def test_convert_usd_to_other_currency_length():
    assert len(convert_usd_to_other_currency(DATAFRAME_STOCK, COUNTRY, START_DATE, END_DATE)) == len(DATAFRAME_STOCK)


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
    assert validation_null_value(DATAFRAME_STOCK) is None
