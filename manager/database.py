import pandas as pd
from manager import utils
import yfinance as yf


def get_database_inflation(country: str, start_date = 0, end_date = -1) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Inflation/{country}_inflation.csv", index_col=0, encoding="iso-8859-1")
    dataframe = dataframe[start_date:end_date][:-1]
    dataframe = utils.convert_index_to_DatetimeIndex(dataframe)
    return dataframe


def get_database_prices(goods: str, start_date = 0, end_date = -1) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Prices/{goods}_global.csv", index_col=0)
    dataframe = dataframe[start_date:end_date]
    dataframe = utils.convert_index_to_DatetimeIndex(dataframe)
    return dataframe


def get_database_stock(stock_list: list[str], start_date, end_date) -> pd.DataFrame:
    multi_stock_data = yf.download(stock_list, start=start_date, end=end_date, interval="1mo", progress=False)['Close']
    if type(multi_stock_data) is pd.core.series.Series:
        multi_stock_data = multi_stock_data.to_frame().rename(columns={"Close": stock_list[0]})
    return multi_stock_data


def get_database_currency_rate_to_dollar(currency_country: str, start_date, end_date) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Currency_rate/{currency_country}_to_usd.csv", index_col=0)
    dataframe = utils.convert_index_to_DatetimeIndex(dataframe)
    dataframe = dataframe[start_date:end_date][:-1]
    dataframe = utils.convert_country_to_currency(dataframe)
    return dataframe


def get_database_currency_index_to_dollar(currency_country: str, start_date, end_date) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Currency_indexed/{currency_country}_usd.csv", index_col=0)
    dataframe = utils.convert_index_to_DatetimeIndex(dataframe)
    dataframe = dataframe[start_date:end_date][:-1]
    dataframe = utils.convert_country_to_currency(dataframe)
    return dataframe

