import yfinance as yf
from functools import wraps


def validation_date(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        dataframe = func(*args, **kwargs)
        start_date = args[1]
        end_date = args[2]
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
    return wrapper


def validation_null_value_in_database(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        dataframe = func(*args, **kwargs)
        if dataframe.empty or dataframe.isna().any().any():
            return "Error in dataframe"
        else:
            return dataframe
    return wrapper


def validate_stock_data(func):
    @wraps(func)
    def wrapper(stock):
        if 'country' in yf.Ticker(stock).info.keys():
            return func(stock)
        else:
            return "No stock info"
    return wrapper
