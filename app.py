import yfinance as yf
from manager import utils, list_of_available, single_value, database

start_data = "2020-01-01"
end_data = "2022-01-01"
country = "poland"
stock_1 = "AAPL"
stock_2 = "11B.WA"

if __name__ == "__main__":
    yf.set_tz_cache_location("data/cache")
    print("Hello")
    stock2 = database.get_database_stock_multi([stock_1], start_data, end_data)
    infla = database.get_database_inflation("USA", start_data, end_data)
    stock2 = utils.concat_database_with_inflation(infla, stock2)
    utils.plotting_database(stock2)
