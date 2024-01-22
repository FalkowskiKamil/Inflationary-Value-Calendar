import os
import pandas as pd

def get_list_of_available_inflation_country_from_file() -> list[str]:
    country_list = os.listdir("data/Inflation")
    country_list = [x.split("_")[0] for x in country_list]
    return country_list


def get_list_of_available_goods_prices_from_file() -> list[str]:
    goods_list = os.listdir("data/Prices")
    goods_list = [x.split("_")[0] for x in goods_list]
    return goods_list


def get_list_of_available_stock_from_file(country: str = None) -> list[str]:
    dataframe = pd.read_csv("data/Stock/stock_listed.csv", index_col=0)
    if country:
        dataframe = dataframe[dataframe["Country"] == country.capitalize()]
    return dataframe


def get_list_of_available_currency_by_country_from_file() -> list[str]:
    currency_list = os.listdir("data/Currency_rate")
    currency_list = [x.split("_")[0] for x in currency_list]
    return currency_list

