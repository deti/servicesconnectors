from unittest import mock

import pytest
import respx
from faker import Faker
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from src.connections.api.appstore import (AppStoreConnectionItem,
                                          build_appstore_url)
from src.connections.models import Connection, create_connection
from src.connections.schemas import ConnectionCreate

fake = Faker()


def fake_appstore_item() -> AppStoreConnectionItem:
    return AppStoreConnectionItem(
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

    response = client.post("/connections/appstore", json=as_dict)

    assert response.status_code == 422


@respx.mock
def test_create_appstore_returns_404_if_not_found(client: TestClient):
    item = fake_appstore_item()

    app_route = respx.get(build_appstore_url(item)).mock(return_value=Response(404))

    response = client.post("/connections/appstore", json=item.model_dump())
    assert app_route.called

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Resource not found",
    }


@respx.mock
def test_create_appstore_connector(client: TestClient, db: Session):
    item = fake_appstore_item()

    app_route = respx.get(build_appstore_url(item)).mock(return_value=Response(200))

    response = client.post("/connections/appstore", json=item.model_dump())
    assert app_route.called

    connector = db.query(Connection).first()
    assert connector is not None

    assert response.status_code == 200
    assert response.json() == {
        "type": "appstore",
        "message": f"Created '{item.description}'",
        "uuid": connector.uuid,
    }


@respx.mock
def test_create_appstore_connector_do_not_create_duplicate(
    client: TestClient, db: Session
):
    item = fake_appstore_item()

    connector_create = ConnectionCreate(
        type="appstore",
        settings={
            "type": "appstore",
            "region": item.region,
            "slug": item.slug,
            "appid": item.appid,
        },
        description=item.description,
    )
    connector = create_connection(db, connector_create)

    app_route = respx.get(build_appstore_url(item)).mock(return_value=Response(200))

    # Ensure connector is not created
    with mock.patch(
        "src.connections.models.create_connection",
    ) as mock_create_connector:
        response = client.post("/connections/appstore", json=item.model_dump())
        assert mock_create_connector.called is False
    assert app_route.called

    assert response.status_code == 200
    assert response.json() == {
        "type": "appstore",
        "message": f"Created '{item.description}'",
        "uuid": connector.uuid,
    }
