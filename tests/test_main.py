""" Test the main.py module """

from fastapi.testclient import TestClient


def test_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "alive"}
