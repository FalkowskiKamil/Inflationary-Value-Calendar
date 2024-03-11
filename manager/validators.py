import yfinance as yf
import pandas as pd
from datetime import date


def validation_date(dataframe, start_date: date = 0, end_date: date = -1):
    if not isinstance(start_date, int) and not isinstance(end_date, int):
        if dataframe.index[0].date() <= start_date:
            if dataframe.index[-1].date() >= end_date:
                dataframe = dataframe[start_date:end_date]
            else:
                end_date = dataframe.index[-1]
                dataframe = dataframe[start_date: end_date]
        else:
            start_date = dataframe.index[0].date()
            dataframe = dataframe[start_date:end_date]

    return dataframe


def validation_null_value(dataframe: pd.DataFrame):
    if dataframe.empty or dataframe.isna().any().any():
        return "Error in dataframe"
    else:
        return dataframe


def validate_stock(func):
    def wrapper(stock):
        if 'country' in yf.Ticker(stock).info.keys():
            return func(stock)
        else:
            return "No stock info"
    return wrapper
