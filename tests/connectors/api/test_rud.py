from unittest.mock import ANY, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.connectors.models import Connection
from tests.connectors.fakes import fake_connector


def add_fake_connector(db: Session) -> Connection:
    connector = fake_connector()
    db.add(connector)
    db.commit()
    db.refresh(connector)
    return connector


def test_get_all_connectors_uuids_gets_nothing(client: TestClient, db: Session):
    response = client.get("/connectors")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_connectors_uuids(client: TestClient, db: Session):
    connector = add_fake_connector(db)

    response = client.get("/connectors")
    assert response.status_code == 200

    assert response.json() == [
        {
            "uuid": connector.uuid,
            "type": connector.type,
            "settings": connector.settings,
            "description": connector.description,
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
    connector = add_fake_connector(db)

    response = client.get(f"/connectors/{connector.uuid}")
    assert response.status_code == 204


def test_get_connector_returns_200_when_fetched(client: TestClient, db: Session):
    connector = add_fake_connector(db)

    with patch("src.connectors.api.rud.Storage") as mock_storage:
        mock_storage().read.return_value = {"test": "test"}
        response = client.get(f"/connectors/{connector.uuid}")
        mock_storage().read.assert_called_once_with(connector.uuid)

    assert response.status_code == 200
    assert response.json() == {"test": "test"}


def test_delete_connector_returns_404_when_not_found(client: TestClient, db: Session):
    response = client.delete("/connectors/test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connector not found"}


def test_delete_connector_returns_200_when_deleted(client: TestClient, db: Session):
    with (
        patch("src.connectors.api.rud.get_connector") as mock_get_connector,
        patch(
            "src.connectors.api.rud.delete_connector_from_db"
        ) as mock_delete_connector_from_db,
        patch("src.connectors.api.rud.Storage") as mock_storage,
    ):
        mock_get_connector.return_value = True
        response = client.delete("/connectors/test-uuid")

        mock_get_connector.assert_called_once_with(ANY, "test-uuid")
        mock_delete_connector_from_db.assert_called_once_with(ANY, "test-uuid")
        mock_storage().delete.assert_called_once_with("test-uuid")

    assert response.status_code == 200
    assert response.json() == {"message": "Deleted test-uuid"}


def test_update_connector_returns_404_when_not_found(client: TestClient, db: Session):
    with patch("src.connectors.api.rud.get_connector") as mock_get_connector:
        mock_get_connector.return_value = None
        response = client.put("/connectors/test-uuid")
        mock_get_connector.assert_called_once_with(ANY, "test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connector not found"}


def test_update_connector_returns_200_when_updated(client: TestClient, db: Session):
    connector = fake_connector()

    with (
        patch("src.connectors.api.rud.get_connector") as mock_get_connector,
        patch("src.connectors.api.rud.run_connector") as mock_run_connector,
    ):
        mock_get_connector.return_value = connector
        response = client.put(f"/connectors/{connector.uuid}")

        mock_get_connector.assert_called_once_with(ANY, connector.uuid)
        mock_run_connector.assert_called_once_with(connector)

    assert response.status_code == 200
    assert response.json() == {"message": f"Updated {connector.uuid}"}
