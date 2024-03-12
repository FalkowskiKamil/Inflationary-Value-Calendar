from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_api_index():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json()["Available API Data"] == {
        "Databases": ["inflation", "goods", "stock", "currency"],
        "List_of_available": ["country", "goods", "currency"],
        "Single_info": ["stock date", "country", "currency", "long name", "last value"],
        "Type of plotting database": {"exchange": ["currency_exchang", "goods_currency_exchange",
                                                   "stock_currency_exchange"],
                                      "inflation": ["currency_rate_to_dollar_with_inflation",
                                                    "goods_value_with_inflation",
                                                    "stock_value_with_inflation"]},
    }


def test_api_stock():
    response = client.post("/api/stock_info/")
    assert response.status_code == 200
    assert response.json() == ['stock date', 'country', 'currency', 'long name', 'last value']
    response = client.post("/api/stock_info/", data={"info_type": "stock date", "stock": "AAPL"})
    assert response.status_code == 200
    assert response.json() == {'stock': 'AAPL', 'stock date': '1985-01-01, 2024-03-01'}


def test_api_database():
    response = client.post("/api/databases/")
    assert response.status_code == 200
    assert response.json() == ["inflation", "goods", "stock", "currency"]
    response = client.post("/api/databases/", data={"databaseType": "goods",
                                                    "databaseKey": "aluminum",
                                                    "stockName": "",
                                                    "startMonth": 1,
                                                    "startYear": 2000,
                                                    "endMonth": 2,
                                                    "endYear": 2000,
                                                    })
    assert response.status_code == 200
    assert response.json() == {
        'aluminum (dollar per metric ton) in USD': {'2000-01-01T00:00:00': 1679.85, '2000-02-01T00:00:00': 1679.425}}


def test_api_list_of_available():
    response = client.post("/api/list_of_available/")
    assert response.status_code == 200
    assert response.json() == {"null": ["country", "goods", "currency"]}
    response = client.post("/api/list_of_available/", data={"list_type": "country"})
    assert response.status_code == 200
    assert response.json() == {'country': ['Australia', 'Austria', 'Belgium',
                                           'Brazil', 'Canada', 'Chile', 'China', 'Columbia', 'Czech', 'Denmark',
                                           'Estonia', 'Euro currency country', 'Finland', 'France', 'Germany',
                                           'Greece', 'Hungrary', 'Iceland', 'India', 'Indonesia', 'Ireland',
                                           'Israel', 'Italy', 'Japan', 'Korea', 'Latvia', 'Luxembourg', 'Mexico',
                                           'Netherland', 'New zealand', 'Norway', 'Poland', 'Portugal', 'Russia',
                                           'Slovak republic', 'Slovenia', 'South africa', 'Spain', 'Sweden',
                                           'Switzerland',
                                           'Turkey', 'United kingdom', 'United states']}


def test_api_plotted_data():
    response = client.post("/api/converted_data/")
    assert response.status_code == 200
    assert response.json() == {"exchange": ["currency_exchang", "goods_currency_exchange",
                                            "stock_currency_exchange"],
                               "inflation": ["currency_rate_to_dollar_with_inflation", "goods_value_with_inflation",
                                             "stock_value_with_inflation"]}
    response = client.post("/api/converted_data/", data={"mainDataframeType": "exchange",
                                                         "mainDataframeTitle": "aluminum",
                                                         "converterCategory": "goods_currency_exchange",
                                                         "currency_target": "PLN",
                                                         "startMonth": 1,
                                                         "startYear": 2000,
                                                         "endMonth": 2,
                                                         "endYear": 2000,
                                                         })
    assert response.status_code == 200
    assert response.json() == {'aluminum (Polish Złoty (PLN) per metric ton)': {'2000-01-01T00:00:00': 6893.264475,
                                                                                '2000-02-01T00:00:00': 6970.413476190475}}
