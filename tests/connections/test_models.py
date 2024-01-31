import json

from faker import Faker
from sqlalchemy.orm import Session

from src.connections.models import (create_connection,
                                    delete_connection_from_db,
                                    get_all_connections, get_connection,
                                    get_or_create_connection)
from src.connections.schemas import ConnectionCreate
from src.connections.utils import generate_uuid_from_dict
from tests.connections.fakes import fake_appstore_settings, fake_connection

fake = Faker()


def test_get_connector_returns_none_when_non_exsited(db: Session):
    connector = get_connection(db, "test-uuid")
    assert connector is None


def test_get_connector_returns_connector_when_exsited(db: Session):
    connector = fake_connection()
    db.add(connector)
    db.commit()
    db.refresh(connector)

    assert get_connection(db, str(connector.uuid)) == connector


def fake_connection_create() -> ConnectionCreate:
    return ConnectionCreate(
        type=fake.word(),
        settings=fake_appstore_settings(),
        description=fake.sentence(),
    )


def test_create_connector_creates_connector(db: Session):
    connector_create = fake_connection_create()

    connector = create_connection(db, connector_create)

    assert connector.type == connector_create.type
    assert connector.settings == json.dumps(connector_create.settings)
    assert connector.description == connector_create.description


def test_or_create_connector_creates_connector_when_not_exsited(db: Session):
    connector_create = fake_connection_create()

    # No Connect before test
    expected_uuid = generate_uuid_from_dict(connector_create.settings)
    assert get_connection(db, expected_uuid) is None

    # Connector created
    connector = get_or_create_connection(db, connector_create)
    assert expected_uuid == connector.uuid
    assert connector.type == connector_create.type
    assert connector.settings == json.dumps(connector_create.settings)
    assert connector.description == connector_create.description


def test_or_create_connector_returns_connector_when_exsited(db: Session):
    connector_create = fake_connection_create()
    created_item = create_connection(db, connector_create)
    retrieved_item = get_or_create_connection(db, connector_create)

    assert retrieved_item == created_item


def test_all_connectors_uuids_returns_empty_list_when_no_connector(db: Session):
    assert get_all_connections(db) == []


def test_get_all_connectors_returns_all_connectrs(db: Session):
    expected_uuids = [
        create_connection(db, fake_connection_create()) for _ in range(10)
    ]
    assert set(get_all_connections(db)) == set(expected_uuids)


def test_delete_connector_from_db_deletes_connector_when_exsited(db: Session):
    connector = create_connection(db, fake_connection_create())
    connector_uuid = str(connector.uuid)  # avoid mypy error
    assert get_connection(db, connector_uuid) is not None

    delete_connection_from_db(db, connector_uuid)
    assert get_connection(db, connector_uuid) is None
