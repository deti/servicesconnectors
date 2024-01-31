from unittest.mock import ANY, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.connections.models import Connection
from tests.connections.fakes import fake_connection


def add_fake_connection(db: Session) -> Connection:
    connection = fake_connection()
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def test_get_all_connections_uuids_gets_nothing(client: TestClient, db: Session):
    response = client.get("/connections")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_connections_uuids(client: TestClient, db: Session):
    connection = add_fake_connection(db)

    response = client.get("/connections")
    assert response.status_code == 200

    assert response.json() == [
        {
            "uuid": connection.uuid,
            "type": connection.type,
            "settings": connection.settings,
            "description": connection.description,
            "created_at": f"{connection.created_at.isoformat()}",
            "modified_at": f"{connection.modified_at.isoformat()}",
        }
    ]


def test_get_connection_returns_404_when_not_found(client: TestClient, db: Session):
    response = client.get("/connections/test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connection not found"}


def test_get_connection_returns_204_when_not_fetched_yet(
    client: TestClient, db: Session
):
    connection = add_fake_connection(db)

    response = client.get(f"/connections/{connection.uuid}")
    assert response.status_code == 204


def test_get_connection_returns_200_when_fetched(client: TestClient, db: Session):
    connection = add_fake_connection(db)

    with patch("src.connections.api.rud.Storage") as mock_storage:
        mock_storage().read.return_value = {"test": "test"}
        response = client.get(f"/connections/{connection.uuid}")
        mock_storage().read.assert_called_once_with(connection.uuid)

    assert response.status_code == 200
    assert response.json() == {"test": "test"}


def test_delete_connection_returns_404_when_not_found(client: TestClient, db: Session):
    response = client.delete("/connections/test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connection not found"}


def test_delete_connection_returns_200_when_deleted(client: TestClient, db: Session):
    with (
        patch("src.connections.api.rud.get_connection") as mock_get_connection,
        patch(
            "src.connections.api.rud.delete_connection_from_db"
        ) as mock_delete_connection_from_db,
        patch("src.connections.api.rud.Storage") as mock_storage,
    ):
        mock_get_connection.return_value = True
        response = client.delete("/connections/test-uuid")

        mock_get_connection.assert_called_once_with(ANY, "test-uuid")
        mock_delete_connection_from_db.assert_called_once_with(ANY, "test-uuid")
        mock_storage().delete.assert_called_once_with("test-uuid")

    assert response.status_code == 200
    assert response.json() == {"message": "Deleted test-uuid"}


def test_update_connection_returns_404_when_not_found(client: TestClient, db: Session):
    with patch("src.connections.api.rud.get_connection") as mock_get_connection:
        mock_get_connection.return_value = None
        response = client.put("/connections/test-uuid")
        mock_get_connection.assert_called_once_with(ANY, "test-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Connection not found"}


def test_update_connection_returns_200_when_updated(client: TestClient, db: Session):
    connection = fake_connection()

    with (
        patch("src.connections.api.rud.get_connection") as mock_get_connection,
        patch("src.connections.api.rud.run_connector") as mock_run_connector,
    ):
        mock_get_connection.return_value = connection
        response = client.put(f"/connections/{connection.uuid}")

        mock_get_connection.assert_called_once_with(ANY, connection.uuid)
        mock_run_connector.assert_called_once_with(connection)

    assert response.status_code == 200
    assert response.json() == {"message": f"Updated {connection.uuid}"}
