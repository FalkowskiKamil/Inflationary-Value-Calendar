from fastapi import APIRouter, Form
from manager.utils import convert_form_date_to_pandas_date_type
from manager.collectors import api_exchange_converter_collector, api_inflation_converter_collector,\
    api_databases_collector, api_stock_collector, api_options_collector

router_api = APIRouter()


@router_api.get("/", tags=["api"])
async def api_index():
    return {"Available API Data": {
        "Databases": ["inflation", "goods", "stock", "currency"],
        "Options": ["country", "goods", "currency"],
        "Single_info": ["stock date", "country", "currency", "long name", "last value"],
        "Type of plotting database": {"exchange": ["currency_exchang", "goods_currency_exchange",
                                                   "stock_currency_exchange"],
                                      "inflation": ["currency_rate_to_dollar_with_inflation", "goods_value_with_inflation",
                                                    "stock_value_with_inflation"]},
    }}


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
        start_date, end_date = convert_form_date_to_pandas_date_type(startYear, startMonth, endYear, endMonth)
    else:
        return (await api_index())["Available API Data"]["Databases"]

    data_list = api_databases_collector(databaseType, databaseKey, stockName, start_date, end_date)
    return data_list


@router_api.post("/options/", tags=["api"])
async def api_options(list_type: str = Form(None)):
    data_list = api_options_collector(list_type)
    if data_list is None:
        data_list = (await api_index())["Available API Data"]["Options"]
    return {list_type: data_list}


@router_api.post("/stock_info/", tags=["api"])
async def api_stock(
        info_type=Form(None),
        stock=Form(None)
):
    result = api_stock_collector(info_type, stock)
    if result is None:
        return (await api_index())["Available API Data"]["Single_info"]
    return {"stock": stock, info_type: result}


@router_api.post("/converted_data", tags=["api"])
async def api_plotted_data(
        mainDataframeType: str = Form(None),
        mainDataframeTitle: str = Form(None),
        converterCategory: str = Form(None),
        currency_target: str = Form(None),
        startMonth: int = Form(None),
        startYear: int = Form(None),
        endMonth: int = Form(None),
        endYear: int = Form(None),

):
    if startMonth:
        start_date, end_date = convert_form_date_to_pandas_date_type(startYear, startMonth, endYear, endMonth)
    else:
        return (await api_index())["Available API Data"]["Type of plotting database"]

    if mainDataframeType == "exchange":
        dataframe = api_exchange_converter_collector(converterCategory, mainDataframeTitle, currency_target, start_date, end_date)
    elif mainDataframeType == "inflation":
        dataframe = api_inflation_converter_collector(converterCategory, mainDataframeTitle, currency_target, start_date, end_date)
    else:
        return (await api_index())["Available API Data"]["Type of plotting database"]
    return dataframe
