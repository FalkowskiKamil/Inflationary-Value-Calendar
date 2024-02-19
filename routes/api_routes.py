from fastapi import APIRouter, Form
from manager import list_of_available_data

router_api = APIRouter()


@router_api.get("/", tags=['api'])
async def api_index():
    return {"Available API Data": {
                "Databases": ["inflation", "goods_prices", "stock", "currency_rate_to_dollar", "currency_index_to_dollar"],
                "List_of_available": ["country", "goods", "currency"]},
                "Single_value": "soon"}


@router_api.post("/databases/", tags=['api'])
async def api_databases(
    database_type: str = Form(...),
    currency: str = Form(...),
    start_month: int = Form(...),
    start_year: int = Form(...),
    end_month: int = Form(...),
    end_year: int = Form(...),
):
    data = {
            "database_type": database_type,
            "currency": currency,
            "start_month": start_month,
            "start_year": start_year,
            "end_month": end_month,
            "end_year": end_year,
    }
    return data


@router_api.get("/list_of_available/{list_type}", tags=["api"])
async def api_list_of_available(list_type: str = "main"):
    if list_type == "inflation":
        data_list = list_of_available_data.get_list_of_available_inflation_country_data()
    elif list_type == "goods_prices":
        data_list = list_of_available_data.get_list_of_available_goods_prices_data()
    elif list_type == "currency_rate_to_dollar" or list_type == "currency_index_to_dollar":
        data_list = sorted(set(list_of_available_data.get_list_of_available_currency_data().values()))
    else:
        list_type = "main"
        data_list = ["country", "goods", "currency by country"]
    return {"list_type": list_type, "list": data_list}
