import os


def get_list_of_available_inflation_country_data() -> list[str]:
    country_list = os.listdir("data/Inflation")
    country_list = [file.split("_inflation")[0] for file in country_list if file.endswith(".csv")]
    return country_list


def get_list_of_available_goods_prices_data() -> list[str]:
    goods_list = os.listdir("data/Prices")
    goods_list = [file.split("_")[0] for file in goods_list if file.endswith(".csv")]
    return goods_list


def get_list_of_available_currency_by_country_data() -> list[str]:
    currency_list = os.listdir("data/Currency_rate")
    currency_list = [file.split("_to_usd")[0] for file in currency_list if file.endswith(".csv")]
    return currency_list
