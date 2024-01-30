from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.connectors.models import Connector


def test_get_all_connectors_uuids_gets_nothing(client: TestClient, db: Session):
    response = client.get("/connectors")
    assert response.status_code == 200
    assert response.json() == {"uuids": []}


def test_get_all_connectors_uuids_gets_one(client: TestClient, db: Session):
    connector = Connector(
        uuid="test-uuid",
        connector_type="appstore",
        connector_settings='{"region": "us", "slug": "test", "appid": "123456"}',
        description="test description",
    )
    db.add(connector)
    db.commit()

    response = client.get("/connectors")
    assert response.status_code == 200
    assert response.json() == {"uuids": ["test-uuid"]}


def test_get_connector_returns_404_when_not_found(client: TestClient, db: Session):
    response = client.get("/connectors/test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connector not found"}


def test_get_connector_returns_204_when_not_fetched_yet(
    client: TestClient, db: Session
):
    connector = Connector(
        uuid="test-uuid",
        connector_type="appstore",
        connector_settings='{"region": "us", "slug": "test", "appid": "123456"}',
        description="test description",
    )
    db.add(connector)
    db.commit()

    response = client.get("/connectors/test-uuid")
    assert response.status_code == 204


def test_get_connector_returns_200_when_fetched(client: TestClient, db: Session):
    connector = Connector(
        uuid="test-uuid",
        connector_type="appstore",
        connector_settings='{"region": "us", "slug": "test", "appid": "123456"}',
        description="test description",
    )
    db.add(connector)
    db.commit()

    with patch("src.connectors.api.rud.Storage") as mock_storage:
        mock_storage().read.return_value = {"test": "test"}
        response = client.get("/connectors/test-uuid")
    assert response.status_code == 200
    assert response.json() == {"test": "test"}
