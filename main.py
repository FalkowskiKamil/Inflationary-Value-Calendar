import yfinance as yf
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.api_routes import router_api
from routes.web_routes import router_web
yf.set_tz_cache_location("data/cache")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_web)
app.include_router(router_api, prefix="/api")
