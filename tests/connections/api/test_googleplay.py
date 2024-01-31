import json

import pytest
import respx
from faker import Faker
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from src.connections.api.googleplay import (GooglePlayConnectionItem,
                                            build_googleplay_url)
from src.connections.models import Connection

fake = Faker()


def fake_googleplay_item() -> GooglePlayConnectionItem:
    return GooglePlayConnectionItem(
        slug=fake.slug(),
        description=fake.sentence(),
    )


def test_build_googleplay_url():
    item = fake_googleplay_item()
    expected_url = f"https://play.google.com/store/apps/details?id={item.slug}"

    url = build_googleplay_url(item)

    assert expected_url == url


@pytest.mark.parametrize(
    "parameter",
    [
        pytest.param("slug", id="slug"),
        pytest.param("description", id="description"),
    ],
)
def test_create_googleplay_missing_parameter_returns_422(
    client: TestClient, parameter: str
):
    item = fake_googleplay_item()
    as_dict = item.model_dump()
    as_dict[parameter] = None

    response = client.post("/connections/googleplay", json=as_dict)

    assert response.status_code == 422


def test_create_googleplay_returns_404_if_not_found(client: TestClient):
    item = fake_googleplay_item()
    url = build_googleplay_url(item)

    with respx.mock:
        respx.get(url).mock(return_value=Response(404))

        response = client.post("/connections/googleplay", json=item.model_dump())

        assert response.status_code == 404


def test_create_googleplay_returns_200_if_found(client: TestClient, db: Session):
    item = fake_googleplay_item()
    url = build_googleplay_url(item)

    with respx.mock:
        respx.get(url).mock(return_value=Response(200))

        response = client.post("/connections/googleplay", json=item.model_dump())

    connection = db.query(Connection).filter(Connection.type == "googleplay").one()
    assert connection.description == item.slug
    assert response.json() == {
        "type": "googleplay",
        "message": f"Created '{item.description}'",
        "uuid": connection.uuid,
    }
    assert response.status_code == 200
    assert json.loads(connection.settings) == {
        "type": "googleplay",
        "slug": item.slug,
    }


def test_create_googleplay_doesnt_create_if_already_exists(
    client: TestClient, db: Session
):
    item = fake_googleplay_item()
    url = build_googleplay_url(item)

    with respx.mock:
        respx.get(url).mock(return_value=Response(200))

        response = client.post("/connections/googleplay", json=item.model_dump())
        assert response.status_code == 200

        response = client.post("/connections/googleplay", json=item.model_dump())
        assert response.status_code == 200

    assert db.query(Connection).filter(Connection.type == "googleplay").count() == 1
