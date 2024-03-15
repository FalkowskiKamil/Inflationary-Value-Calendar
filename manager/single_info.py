import yfinance as yf
from manager.validators import validate_stock_data
from data.currency_country import currency_dict_short


@validate_stock_data
def get_date_of_stock_data(stock: str) -> (str, str):
    stock_data = yf.download(stock, interval="1mo", progress=False)["Close"]
    return f'{stock_data.index[0].date()}, {stock_data.index[-1].date()}'


@validate_stock_data
def get_stock_country(stock: str) -> str:
    country = yf.Ticker(stock).info["country"].lower()
    if " " in country:
        country = country.replace(" ", "_")
    return country


@validate_stock_data
def get_stock_currency(stock: str) -> str:
    currency = yf.Ticker(stock).info["currency"]
    return currency


@validate_stock_data
def get_stock_longname(stock: str) -> str:
    name = yf.Ticker(stock).info["longName"]
    return name


@validate_stock_data
def get_stock_last_value(stock_name: str) -> float:
    stock_data = yf.Ticker(stock_name)
    return stock_data.history(period="1d")["Close"].iloc[0]


def finding_country_by_currency(currency: str) -> str:
    country = list(currency_dict_short.keys())[list(currency_dict_short.values()).index(currency)].replace(" ", "_")
    return country
