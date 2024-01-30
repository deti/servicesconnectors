from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.connectors.models import Connector


def test_get_all_connectors_uuids_gets_nothing(client: TestClient, db: Session):
    response = client.get("/connectors")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_connectors_uuids(client: TestClient, db: Session):
    connector = Connector(
        uuid="test-uuid",
        connector_type="appstore",
        connector_settings='{"region": "us", "slug": "test", "appid": "123456"}',
        description="test description",
    )
    db.add(connector)
    db.commit()
    db.refresh(connector)

    response = client.get("/connectors")
    assert response.status_code == 200

    assert response.json() == [
        {
            "uuid": "test-uuid",
            "connector_type": "appstore",
            "connector_settings": '{"region": "us", "slug": "test", "appid": "123456"}',
            "description": "test description",
            "created_at": f"{connector.created_at.isoformat()}",
            "modified_at": f"{connector.modified_at.isoformat()}",
        }
    ]


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


def test_delete_connector_returns_404_when_not_found(client: TestClient, db: Session):
    response = client.delete("/connectors/test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connector not found"}


def test_delete_connector_returns_200_when_deleted(client: TestClient, db: Session):
    with patch("src.connectors.api.rud.get_connector") as mock_get_connector, patch(
        "src.connectors.api.rud.delete_connector_from_db"
    ) as mock_delete_connector_from_db, patch(
        "src.connectors.api.rud.Storage"
    ) as mock_storage:

        mock_get_connector.return_value = True
        mock_delete_connector_from_db.return_value = None
        mock_storage().delete.return_value = None
        response = client.delete("/connectors/test-uuid")

        mock_storage().delete.assert_called_once_with("test-uuid")

    assert response.status_code == 200
    assert response.json() == {"message": "Deleted test-uuid"}


def test_update_connector_returns_404_when_not_found(client: TestClient, db: Session):
    response = client.put("/connectors/test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connector not found"}
