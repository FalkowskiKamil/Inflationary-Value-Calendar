from fastapi import Request, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from manager import utils, list_of_available_data, database
from routes.api_routes import api_index

router_web = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_web.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router_web.get("/databases/", response_class=HTMLResponse)
async def database_main(request: Request, api_data: dict = Depends(api_index)):
    return templates.TemplateResponse(
        request=request, name="database_main.html", context={"database_list": api_data["Available API Data"]["Databases"]}
    )


@router_web.post("/databases/")
async def databases(
    request: Request,
    databaseType: str = Form(...),
    databaseKey: str = Form(None),
    stockName: str = Form(None),
    currency: str = Form(...),
    startMonth: int = Form(...),
    startYear: int = Form(...),
    endMonth: int = Form(...),
    endYear: int = Form(...),
):
    start_date = pd.to_datetime(f"{startYear}-{startMonth}-1").date()
    end_date = pd.to_datetime(f"{endYear}-{endMonth}-1").date()
    if databaseType == "inflation":
        data_list = database.get_database_inflation(databaseKey, start_date, end_date)
    elif databaseType == "goods_prices":
        data_list = database.get_database_prices(databaseKey, start_date, end_date)
    elif databaseType == "stock":
        data_list = database.get_database_stock(stockName, start_date, end_date)
    elif databaseType == "currency_rate_to_dollar":
        database_key = utils.convert_currency_to_country(databaseKey)
        data_list = database.get_database_currency_rate_to_dollar(database_key, start_date, end_date)
    elif databaseType == "currency_key_to_dollar":
        database_key = utils.convert_currency_to_country(databaseKey)
        data_list = database.get_database_currency_index_to_dollar(database_key, start_date, end_date)
    else:
        data_list = ["inflation", "goods_prices", "stock", "currency_rate_to_dollar", "currency_key_to_dollar"]
    return templates.TemplateResponse("database.html", {"request": request, "database": data_list})


@router_web.get("/list_of_available/", response_class=HTMLResponse)
async def list_of_available_main(request: Request, api_data: dict = Depends(api_index)):
    return templates.TemplateResponse(
        request=request,
        name="list_of_available_main.html",
        context={"api_data": api_data["Available API Data"]["List_of_available"]}
    )


@router_web.get("/list_of_available/{list_type}", response_class=HTMLResponse)
async def list_of_available(request: Request, list_type: str):
    if list_type == "country":
        data_list = list_of_available_data.get_list_of_available_inflation_country_data()
    elif list_type == "goods":
        data_list = list_of_available_data.get_list_of_available_goods_prices_data()
    elif list_type == "currency":
        data_list = set(list_of_available_data.get_list_of_available_currency_data().values())
    else:
        return await list_of_available_main(request)
    return templates.TemplateResponse(
        request=request, name="list_of_available.html", context={"list": data_list, "list_type": list_type}
    )


@router_web.get("/plotly_view/")
async def plotly_view(request: Request):
    return templates.TemplateResponse(
        request=request, name="plot_view.html"
    )
