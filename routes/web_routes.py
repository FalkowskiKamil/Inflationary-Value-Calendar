from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from manager import utils
from routes.api_routes import api_index, api_databases, \
    api_stock, api_options

router_web = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_web.get("/", response_class=HTMLResponse, tags=["web"])
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router_web.get("/databases/", response_class=HTMLResponse, tags=["web"])
async def database_main(request: Request, api_data: dict = Depends(api_index)):
    return templates.TemplateResponse(
        request=request, name="database_main.html", context={"database_list": api_data["Available API Data"]["Databases"]})


@router_web.post("/databases/", response_class=HTMLResponse, tags=["web"])
async def databases(
    request: Request,
    api_data=Depends(api_databases)
):
    if type(api_data) is pd.DataFrame:
        api_data = utils.plotting_dataframe(api_data)
    return templates.TemplateResponse(request=request,
                                      name="database.html",
                                      context={"database": api_data})


@router_web.get("/options/", response_class=HTMLResponse, tags=["web"])
async def options_main(request: Request, api_data: dict = Depends(api_index)):
    return templates.TemplateResponse(
        request=request,
        name="options_main.html",
        context={"api_data": api_data["Available API Data"]["Options"]}
    )


@router_web.post("/options/", response_class=HTMLResponse, tags=["web"])
async def options(request: Request, api_data: dict = Depends(api_options)):
    return templates.TemplateResponse(
        request=request, name="options.html", context={"list": api_data}
    )


@router_web.get("/stock_info/", response_class=HTMLResponse, tags=["web"])
async def stock_info_main(request: Request, api_data: dict = Depends(api_stock)):
    return templates.TemplateResponse(
        request=request,
        name="stock_info_main.html",
        context={"api_data": api_data}
    )


@router_web.post("/stock_info/", response_class=HTMLResponse, tags=["web"])
async def stock_info(request: Request, api_data: dict = Depends(api_stock)):
    return templates.TemplateResponse(
        request=request,
        name="stock_info.html",
        context={"api_data": api_data}
    )


@router_web.get("/plotly_view/", response_class=HTMLResponse, tags=["web"])
async def plotly_view(request: Request):
    return templates.TemplateResponse(
        request=request, name="plot_view.html"
    )
