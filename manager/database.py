import pandas as pd
from manager import utils
import yfinance as yf
from datetime import date


def get_database_inflation(country: str, start_date: date = 0, end_date: date = -1) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Inflation/{country}_inflation.csv", index_col=0, encoding="iso-8859-1", parse_dates=True).rename(columns={"Inflation":f"Inflation in {country}"})
    dataframe = utils.validation_date(dataframe, start_date, end_date)
    utils.validation_null_value(dataframe)
    return dataframe


def get_database_prices(goods: str, start_date: date = 0, end_date: date = -1) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Prices/{goods}_global.csv", index_col=0, parse_dates=True)
    dataframe = utils.validation_date(dataframe, start_date, end_date)
    utils.validation_null_value(dataframe)
    return dataframe


def get_database_stock(stock: str, start_date: date = 0, end_date: date = -1) -> pd.DataFrame:
    try:
        stock_data = yf.download(stock, start=start_date, end=end_date, interval="1mo", progress=False)["Close"]
        stock_data = stock_data.to_frame().rename(columns={"Close": stock})
        utils.validation_null_value(stock_data)
    except Exception as e:
        stock_data = e
    return stock_data


def get_database_currency_rate_to_dollar(currency_country: str, start_date: date = 0, end_date: date = -1) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Currency_rate/{currency_country}_to_usd.csv", index_col=0, parse_dates=True)
    dataframe = utils.validation_date(dataframe, start_date, end_date)
    dataframe = utils.convert_country_to_currency(dataframe)
    utils.validation_null_value(dataframe)
    return dataframe


def get_database_currency_index_to_dollar(currency_country: str, start_date: date = 0, end_date: date = -1) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Currency_indexed/{currency_country}_usd.csv", index_col=0, parse_dates=True)
    dataframe = utils.validation_date(dataframe, start_date, end_date)
    dataframe = utils.convert_country_to_currency(dataframe)
    utils.validation_null_value(dataframe)
    return dataframe
