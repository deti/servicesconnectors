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
