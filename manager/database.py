import pandas as pd
from manager.validators import validation_date, validation_null_value
import yfinance as yf
from datetime import date
from data.currency_country import currency_dict


def get_database_inflation(country: str, start_date: date, end_date: date) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Inflation/{country.replace(' ', '_')}_inflation.csv", index_col=0, encoding="iso-8859-1", parse_dates=True).rename(columns={"Inflation": f"Inflation in {country}"})
    dataframe = validation_date(dataframe, start_date, end_date)
    dataframe = validation_null_value(dataframe)
    return dataframe


def get_database_prices(goods: str, start_date: date, end_date: date, currency="USD") -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Prices/{goods}.csv", index_col=0, parse_dates=True)
    dataframe = dataframe.rename(columns={dataframe.columns[0]: f'{dataframe.columns[0].replace("_", " ")} in {currency}'})
    dataframe = validation_date(dataframe, start_date, end_date)
    dataframe = validation_null_value(dataframe)
    return dataframe


def get_database_stock(stock: str, start_date: date, end_date: date) -> pd.DataFrame:
    stock_data = yf.download(stock, start=start_date, end=end_date, interval="1mo", progress=False)["Close"]
    stock_data = stock_data.to_frame().rename(columns={"Close": f'{stock}'})
    stock_data = validation_null_value(stock_data)
    return stock_data


def get_database_currency_rate_to_dollar(currency_country: str, start_date: date, end_date: date) -> pd.DataFrame:
    dataframe = pd.read_csv(f"data/Currency_rate/{currency_country}_to_usd.csv", index_col=0, parse_dates=True)
    dataframe.rename(columns={currency_country: f"{currency_dict[dataframe.columns[0]]}"}, inplace=True)
    dataframe = validation_date(dataframe, start_date, end_date)
    dataframe = validation_null_value(dataframe)
    return dataframe
