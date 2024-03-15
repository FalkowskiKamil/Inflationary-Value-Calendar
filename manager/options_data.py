import os
from data.currency_country import currency_dict


def get_options_country_with_currency_data() -> list[str]:
    country_list = os.listdir("data/Currency_rate")
    country_list = [file.split("_to_usd")[0].capitalize() for file in country_list if file.endswith(".csv")]
    return country_list


def get_options_currency_data() -> dict:
    return currency_dict


def get_options_inflation_country_data() -> list[str]:
    country_list = os.listdir("data/Inflation")
    country_list = [file.split("_inflation")[0].capitalize().replace("_", " ") for file in country_list if file.endswith(".csv")]
    return country_list


def get_options_goods_prices_data() -> list[str]:
    goods_list = os.listdir("data/Prices")
    goods_list = [file.split(".csv")[0].capitalize().replace("_", " ") for file in goods_list if file.endswith(".csv")]
    return goods_list
