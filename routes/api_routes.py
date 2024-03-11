from fastapi import APIRouter, Form
from manager import list_of_available_data, database, utils, single_info
import pandas as pd

router_api = APIRouter()


@router_api.get("/", tags=["api"])
async def api_index():
    return {"Available API Data": {
        "Databases": ["inflation", "goods", "stock", "currency"],
        "List_of_available": ["country", "goods", "currency"],
        "Single_info": ["stock date", "country", "currency", "long name", "last value"]}}


@router_api.post("/stock_info/", tags=["api"])
async def api_stock(
        info_type=Form(None),
        stock=Form(None)
):
    if info_type == "stock date":
        result = single_info.get_date_of_stock_data(stock)
    elif info_type == "country":
        result = single_info.get_stock_country(stock)
    elif info_type == "currency":
        result = single_info.get_stock_currency(stock)
    elif info_type == "long name":
        result = single_info.get_stock_longname(stock)
    elif info_type == "last value":
        result = single_info.get_stock_last_value(stock)
    else:
        info_type = "Available info"
        result = (await api_index())["Available API Data"]["Single_info"]
    return {"stock": stock, info_type: result}


@router_api.post("/databases/", tags=["api"])
async def api_databases(
        databaseType: str = Form(None),
        databaseKey: str = Form(None),
        stockName: str = Form(None),
        startMonth: int = Form(None),
        startYear: int = Form(None),
        endMonth: int = Form(None),
        endYear: int = Form(None),
):
    if startMonth:
        start_date = pd.to_datetime(f"{startYear}-{startMonth}-1").date()
        end_date = pd.to_datetime(f"{endYear}-{endMonth}-1").date()
    else:
        return (await api_index())["Available API Data"]["Databases"]

    if databaseType == "inflation" or databaseType == "country":
        data_list = database.get_database_inflation(databaseKey, start_date, end_date)
    elif databaseType == "goods":
        data_list = database.get_database_prices(databaseKey.replace(" ", "_"), start_date, end_date)
    elif databaseType == "stock":
        data_list = database.get_database_stock(stockName, start_date, end_date)
    elif databaseType == "currency":
        country = utils.finding_country_by_currency(databaseKey)
        data_list = database.get_database_currency_rate_to_dollar(country, start_date, end_date)
    else:
        data_list = "Error"
    return data_list


@router_api.post("/list_of_available/", tags=["api"])
async def api_list_of_available(list_type: str = Form(None)):
    if list_type == "country" or list_type == "inflation":
        data_list = list_of_available_data.get_list_of_available_inflation_country_data()
    elif list_type == "goods":
        data_list = list_of_available_data.get_list_of_available_goods_prices_data()
    elif list_type == "currency":
        data_list = sorted(set(list_of_available_data.get_list_of_available_currency_data().values()))
    else:
        list_type = "Main List"
        data_list = (await api_index())["Available API Data"]["List_of_available"]
    return {list_type: data_list}


@router_api.post("/converted_data", tags=["api"])
async def api_plotted_data(
        mainDataframeType: str = Form(None),
        mainDataframeTitle: str = Form(None),
        converterCategory: str = Form(None),
        to_currency: str = Form(None),
        startMonth: int = Form(None),
        startYear: int = Form(None),
        endMonth: int = Form(None),
        endYear: int = Form(None),

):
    start_dataframe_date = None
    end_dataframe_date = None

    if startMonth:
        start_dataframe_date = pd.to_datetime(f"{startYear}-{startMonth}-1").date()
        end_dataframe_date = pd.to_datetime(f"{endYear}-{endMonth}-1").date()

    if converterCategory == "currency_exchange":
        dataframe = utils.finding_exchanging_rate(mainDataframeTitle, to_currency, start_dataframe_date, end_dataframe_date)
        return dataframe
    elif converterCategory == "goods_currency_exchange":
        goods_dataframe = database.get_database_prices(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        currency_exchange_rate_dataframe = utils.finding_exchanging_rate("USD", to_currency, start_dataframe_date, end_dataframe_date)
        dataframe = utils.concat_dataframe_with_exchange_rate(goods_dataframe, currency_exchange_rate_dataframe)
        return dataframe
    elif converterCategory == "stock_currency_exchange":
        stock_dataframe = database.get_database_stock(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        stock_currency = single_info.get_stock_currency(mainDataframeTitle)
        currency_exchange_rate_dataframe = utils.finding_exchanging_rate(stock_currency, to_currency, start_dataframe_date, end_dataframe_date)
        dataframe = utils.concat_dataframe_with_exchange_rate(stock_dataframe, currency_exchange_rate_dataframe)
        return dataframe

    # Inflation
    elif converterCategory == "currency_rate_to_dollar_with_inflation":
        country = single_info.finding_country_by_currency(mainDataframeTitle)
        dataframe_rate = utils.finding_exchanging_rate(mainDataframeTitle, "USD", start_dataframe_date, end_dataframe_date)
        dataframe_inflation = database.get_database_inflation(country, start_dataframe_date, end_dataframe_date)
        dataframe_inflation = utils.indexing_on_start_date(dataframe_inflation)
        dataframe_full = utils.concat_dataframe_with_inflation(dataframe_inflation, dataframe_rate)
        return dataframe_full

    elif converterCategory == "goods_value_with_inflation":
        dataframe = database.get_database_prices(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        exchange_rate = utils.finding_exchanging_rate("USD", to_currency, start_dataframe_date, end_dataframe_date)
        dataframe = utils.concat_dataframe_with_exchange_rate(dataframe, exchange_rate)
        country = utils.finding_country_by_currency(to_currency)
        dataframe_inflation = database.get_database_inflation(country, start_dataframe_date, end_dataframe_date)
        dataframe_inflation = utils.indexing_on_start_date(dataframe_inflation)
        dataframe = utils.concat_dataframe_with_inflation(dataframe_inflation, dataframe)
        return dataframe

    elif converterCategory == "stock_value_with_inflation":
        dataframe = database.get_database_stock(mainDataframeTitle, start_dataframe_date, end_dataframe_date)
        currency = single_info.get_stock_currency(mainDataframeTitle)
        country = single_info.finding_country_by_currency(currency)
        if currency != to_currency:
            exchanging_rate_dataframe = utils.finding_exchanging_rate(currency, to_currency, start_dataframe_date, end_dataframe_date)
            dataframe = utils.concat_dataframe_with_exchange_rate(dataframe, exchanging_rate_dataframe)
        dataframe_inflation = database.get_database_inflation(country, start_dataframe_date, end_dataframe_date)
        dataframe_inflation = utils.indexing_on_start_date(dataframe_inflation)
        dataframe = utils.concat_dataframe_with_inflation(dataframe_inflation, dataframe)
        return dataframe
