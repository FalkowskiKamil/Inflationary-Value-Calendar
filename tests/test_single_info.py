from manager.single_info import get_stock_country, get_stock_currency,\
    get_stock_longname, get_stock_last_value,\
    get_date_of_stock_data, finding_country_by_currency
import pandas as pd

START_DATE = "2010-01-01"
END_DATE = "2015-01-01"
COUNTRY = "poland"
STOCK = "ALE.WA"
CURRENCY = "PLN"
DATABASE = pd.read_csv(f"data/Inflation/{COUNTRY}_inflation.csv", index_col=0, encoding="iso-8859-1")


def test_get_date_of_stock_date():
    date = get_date_of_stock_data(STOCK)
    assert date == "2020-11-01, 2024-03-01"


def test_get_stock_country():
    country = get_stock_country(STOCK)
    assert country == "luxembourg"


def test_get_stock_currency():
    currency = get_stock_currency(STOCK)
    assert currency == "PLN"


def test_get_stock_longmame():
    name = get_stock_longname(STOCK)
    assert name == "Allegro.eu SA"


def test_get_stock_last_value():
    assert get_stock_last_value(STOCK) > 0


def test_finding_country_by_currency():
    country = finding_country_by_currency(CURRENCY)
    print(country)
    assert country == "Poland"
