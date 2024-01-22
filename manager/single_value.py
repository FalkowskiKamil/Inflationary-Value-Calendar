import yfinance as yf
import pandas as pd


def get_value_of_inflation_during_time(dataframe: pd.DataFrame) -> float:
    start_value = dataframe.iloc[0]
    end_value = dataframe.iloc[-1]
    difference = ((end_value - start_value) / start_value)*100
    return difference.values[0]


def get_stock_last_value(stock_name: str) -> float:
    stock_data = yf.Ticker(stock_name)
    return stock_data.history(period="1d")['Close'].iloc[0]
