from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_web_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>Index</title>" in response.text


def test_web_database_main():
    response = client.get("/databases/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>Database</title>" in response.text


def test_web_database():
    response = client.post("/databases/", data={"databaseType": "currency",
                                                    "databaseKey": "PLN",
                                                    "stockName": "",
                                                    "startMonth": "",
                                                    "startYear": 2000,
                                                    "endMonth": 2,
                                                    "endYear": 2000,
                                                })
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>\nDatabase\n</title>" in response.text


def test_web_list_of_available_main():
    response = client.get("/list_of_available/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>\nMain List of Available\n</title>" in response.text


def test_web_list_of_available():
    response = client.post("/list_of_available/", data={"list_type": "country"})
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>\nCountry\n</title>" in response.text


def test_web_stock_info_main():
    response = client.get("/stock_info/",)
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>\nStock info\n</title>" in response.text

def test_web_stock_info():
    response = client.post("/stock_info/", data={"info_type": "long name",
                                                 "stock": "Apple inc."})
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "<title>\nApple inc.\n</title>" in response.text
