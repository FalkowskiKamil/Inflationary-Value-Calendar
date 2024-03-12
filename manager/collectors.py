from manager.database import get_database_currency_rate_to_dollar, get_database_prices,\
        get_database_stock, get_database_inflation

from manager.list_of_available_data import get_list_of_available_currency_data, get_list_of_available_goods_prices_data,\
    get_list_of_available_inflation_country_data


from manager.single_info import get_stock_longname, get_date_of_stock_data,\
        get_stock_currency, get_stock_country, \
        get_stock_last_value, finding_country_by_currency

from manager.utils import finding_exchanging_rate, concat_dataframe_with_exchange_rate,\
        concat_dataframe_with_inflation, indexing_on_start_date


from datetime import date
import pandas as pd


def api_exchange_converter_collector(converterCategory: str, mainDataframeTitle: str, to_currency: str, start_dataframe_date: date, end_dataframe_date: date) -> pd.DataFrame:
    if converterCategory == "currency_exchange":
        dataframe = finding_exchanging_rate(mainDataframeTitle, to_currency, start_dataframe_date, end_dataframe_date)

    elif converterCategory == "goods_currency_exchange":
        goods_dataframe = get_database_prices(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        currency_exchange_rate_dataframe = finding_exchanging_rate("USD", to_currency, start_dataframe_date, end_dataframe_date)
        dataframe = concat_dataframe_with_exchange_rate(goods_dataframe, currency_exchange_rate_dataframe)

    elif converterCategory == "stock_currency_exchange":
        stock_dataframe = get_database_stock(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        stock_currency = get_stock_currency(mainDataframeTitle)
        currency_exchange_rate_dataframe = finding_exchanging_rate(stock_currency, to_currency, start_dataframe_date, end_dataframe_date)
        dataframe = concat_dataframe_with_exchange_rate(stock_dataframe, currency_exchange_rate_dataframe)

    else:
        dataframe = f"{converterCategory} is invalid type of converter"
    return dataframe


def api_inflation_converter_collector(converterCategory: str, mainDataframeTitle: str, to_currency: str, start_dataframe_date: date, end_dataframe_date: date) -> pd.DataFrame:
    if converterCategory == "currency_rate_to_dollar_with_inflation":
        country = finding_country_by_currency(mainDataframeTitle)
        dataframe_rate = finding_exchanging_rate(mainDataframeTitle, "USD", start_dataframe_date, end_dataframe_date)
        dataframe_inflation = get_database_inflation(country, start_dataframe_date, end_dataframe_date)
        dataframe_inflation = indexing_on_start_date(dataframe_inflation)
        dataframe = concat_dataframe_with_inflation(dataframe_inflation, dataframe_rate)

    elif converterCategory == "goods_value_with_inflation":
        dataframe = get_database_prices(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        exchange_rate = finding_exchanging_rate("USD", to_currency, start_dataframe_date, end_dataframe_date)
        dataframe = concat_dataframe_with_exchange_rate(dataframe, exchange_rate)
        country = finding_country_by_currency(to_currency)
        dataframe_inflation = get_database_inflation(country, start_dataframe_date, end_dataframe_date)
        dataframe_inflation = indexing_on_start_date(dataframe_inflation)
        dataframe = concat_dataframe_with_inflation(dataframe_inflation, dataframe)

    elif converterCategory == "stock_value_with_inflation":
        dataframe = get_database_stock(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        currency = get_stock_currency(mainDataframeTitle)
        country = finding_country_by_currency(currency)
        if currency != to_currency:
            exchanging_rate_dataframe = finding_exchanging_rate(currency, to_currency, start_dataframe_date, end_dataframe_date)
            dataframe = concat_dataframe_with_exchange_rate(dataframe, exchanging_rate_dataframe)
        dataframe_inflation = get_database_inflation(country, start_dataframe_date, end_dataframe_date)
        dataframe_inflation = indexing_on_start_date(dataframe_inflation)
        dataframe = concat_dataframe_with_inflation(dataframe_inflation, dataframe)

    else:
        dataframe = f"{converterCategory} is invalid type of converter"
    return dataframe


def api_databases_collector(databaseType: str, databaseKey: str, stockName: str, start_date: date, end_date: date) -> pd.DataFrame:
    if databaseType == "inflation" or databaseType == "country":
        data_list = get_database_inflation(databaseKey, start_date, end_date)
        data_list = indexing_on_start_date(data_list)
    elif databaseType == "goods":
        data_list = get_database_prices(databaseKey.replace(" ", "_"), start_date, end_date)
    elif databaseType == "stock":
        data_list = get_database_stock(stockName, start_date, end_date)
    elif databaseType == "currency":
        country = finding_country_by_currency(databaseKey)
        data_list = get_database_currency_rate_to_dollar(country, start_date, end_date)
    else:
        data_list = f"{databaseType} is invalid type of database"
    return data_list


def api_stock_collector(info_type: str, stock: str) -> str:
    if info_type == "stock date":
        result = get_date_of_stock_data(stock)
    elif info_type == "country":
        result = get_stock_country(stock)
    elif info_type == "currency":
        result = get_stock_currency(stock)
    elif info_type == "long name":
        result = get_stock_longname(stock)
    elif info_type == "last value":
        result = get_stock_last_value(stock)
    else:
        result = None
    return result


def api_list_of_available_collector(list_type: str) -> list:
    if list_type == "country" or list_type == "inflation":
        data_list = get_list_of_available_inflation_country_data()
    elif list_type == "goods":
        data_list = get_list_of_available_goods_prices_data()
    elif list_type == "currency":
        data_list = sorted(set(get_list_of_available_currency_data().values()))
    else:
        data_list = None
    return data_list
