import yfinance as yf
import pandas as pd


def get_date_of_stock_data(stock: str) -> (str, str):
    stock_data = yf.download(stock, interval="1mo", progress=False)["Close"]
    return stock_data.index[0].date(), stock_data.index[-1].date()


def get_stock_country(stock: str) -> str:
    country = yf.Ticker(stock).info["country"].lower()
    if " " in country:
        country = country.replace(" ", "_")
    return country


def get_stock_currency(stock: str) -> str:
    currency = yf.Ticker(stock).info["currency"]
    return currency


def get_stock_longname(stock: str) -> str:
    name = yf.Ticker(stock).info["longName"]
    return name


def get_stock_last_value(stock_name: str) -> float:
    stock_data = yf.Ticker(stock_name)
    return stock_data.history(period="1d")["Close"].iloc[0]


def get_value_of_inflation_during_time(dataframe: pd.DataFrame) -> float:
    start_value = dataframe.iloc[0]
    end_value = dataframe.iloc[-1]
    difference = ((end_value - start_value) / start_value)*100
    return difference.values[0]
