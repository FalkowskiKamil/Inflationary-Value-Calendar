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
        data_list = utils.indexing_on_start_date(data_list)
    elif databaseType == "goods":
        data_list = database.get_database_prices(databaseKey, start_date, end_date)
    elif databaseType == "stock":
        data_list = database.get_database_stock(stockName, start_date, end_date)
    elif databaseType == "currency":
        data_list = database.get_database_currency_rate_to_dollar(databaseKey, start_date, end_date)
    else:
        data_list = "Error"
    return data_list


@router_api.get("/list_of_available/", tags=["api"])
async def api_list_of_available(list_type: str = "main"):
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
        mainDatabaseType: str = Form(None),
        mainDatabaseTitle: str = Form(None),
        extraDatabaseType: str = Form(None),
        extraDatabaseTitle: str = Form(None)

):
    if mainDatabaseType == "goods":
        db = database.get_database_prices(mainDatabaseTitle)
    elif mainDatabaseType == "stock":
        db = database.get_database_stock(mainDatabaseTitle)
    elif mainDatabaseType == "currency":
        db = database.get_database_currency_rate_to_dollar(mainDatabaseTitle)
    elif mainDatabaseType == "inflation":
        db = database.get_database_inflation(mainDatabaseTitle)
    else:
        return "No such databaseType"
    if extraDatabaseType == "currency":
        # Obecnie jest chyba zrobione tylko dla stoka to conver_currency_to_country
        country = utils.convert_currency_to_country(extraDatabaseTitle)
        db2 = utils.convert_usd_to_other_currency(db, country)
    return {"db2": db2}
