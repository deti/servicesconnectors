import pytest
import respx
from faker import Faker
from fastapi.testclient import TestClient
from httpx import Response

from src.connectors.api.appstore import AppStoreItem, build_appstore_url

fake = Faker()


def fake_appstore_item() -> AppStoreItem:
    return AppStoreItem(
        region=fake.country_code().lower(),
        slug=fake.slug(),
        appid=f"id{fake.random_int()}",
        description=fake.sentence(),
    )


def test_build_appstore_url():
    item = fake_appstore_item()
    expected_url = f"https://apps.apple.com/{item.region}/app/{item.slug}/{item.appid}"

    url = build_appstore_url(item)

    assert expected_url == url


@pytest.mark.parametrize(
    "parameter",
    [
        pytest.param("region", id="region"),
        pytest.param("slug", id="slug"),
        pytest.param("appid", id="appid"),
        pytest.param("description", id="description"),
    ],
)
def test_create_appstore_missing_parameter_returns_422(
    client: TestClient, parameter: str
):
    item = fake_appstore_item()
    as_dict = item.model_dump()
    as_dict[parameter] = None

    response = client.post("/connectors/appstore", json=as_dict)

    assert response.status_code == 422


@respx.mock
def test_create_appstore_returns_404_if_not_found(client: TestClient):
    item = fake_appstore_item()

    app_route = respx.get(build_appstore_url(item)).mock(return_value=Response(404))

    response = client.post("/connectors/appstore", json=item.model_dump())
    assert app_route.called

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Resource not found",
    }


@respx.mock
def test_create_appstore_connector(client: TestClient):
    item = fake_appstore_item()

    app_route = respx.get(build_appstore_url(item)).mock(return_value=Response(200))

    response = client.post("/connectors/appstore", json=item.model_dump())
    assert app_route.called

    assert response.status_code == 200
    assert response.json() == {
        "connector_type": "appstore",
        "message": f"Created '{item.description}'",
    }
