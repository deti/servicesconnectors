import json

from faker import Faker
from sqlalchemy.orm import Session

from src.connectors.models import (Connector, create_connector,
                                   delete_connector_from_db,
                                   get_all_connectors, get_connector,
                                   get_or_create_connector)
from src.connectors.schemas import ConnectorCreate
from src.connectors.utils import generate_uuid_from_dict
from tests.connectors.fakes import (fake_appstore_connector_settings,
                                    fake_connector)

fake = Faker()


def test_get_connector_returns_none_when_non_exsited(db: Session):
    connector = get_connector(db, "test-uuid")
    assert connector is None


def test_get_connector_returns_connector_when_exsited(db: Session):
    connector = fake_connector()
    db.add(connector)
    db.commit()
    db.refresh(connector)

    assert get_connector(db, connector.uuid) == connector


def fake_connector_create() -> ConnectorCreate:
    return ConnectorCreate(
        connector_type=fake.word(),
        connector_settings=fake_appstore_connector_settings(),
        description=fake.sentence(),
    )


def test_create_connector_creates_connector(db: Session):
    connector_create = fake_connector_create()

    connector = create_connector(db, connector_create)

    assert connector.connector_type == connector_create.connector_type
    assert connector.connector_settings == json.dumps(
        connector_create.connector_settings
    )
    assert connector.description == connector_create.description


def test_or_create_connector_creates_connector_when_not_exsited(db: Session):
    connector_create = fake_connector_create()

    # No Connect before test
    expected_uuid = generate_uuid_from_dict(connector_create.connector_settings)
    assert get_connector(db, expected_uuid) is None

    # Connector created
    connector = get_or_create_connector(db, connector_create)
    assert expected_uuid == connector.uuid
    assert connector.connector_type == connector_create.connector_type
    assert connector.connector_settings == json.dumps(
        connector_create.connector_settings
    )
    assert connector.description == connector_create.description


def test_or_create_connector_returns_connector_when_exsited(db: Session):
    connector_create = fake_connector_create()
    created_item = create_connector(db, connector_create)
    retrieved_item = get_or_create_connector(db, connector_create)

    assert retrieved_item == created_item


def test_all_connectors_uuids_returns_empty_list_when_no_connector(db: Session):
    assert get_all_connectors(db) == []


def test_get_all_connectors_returns_all_connectrs(db: Session):
    expected_uuids = [create_connector(db, fake_connector_create()) for _ in range(10)]
    assert set(get_all_connectors(db)) == set(expected_uuids)


def test_delete_connector_from_db_deletes_connector_when_exsited(db: Session):
    connector = create_connector(db, fake_connector_create())
    connector_uuid = str(connector.uuid)  # avoid mypy error
    assert get_connector(db, connector_uuid) is not None

    delete_connector_from_db(db, connector_uuid)
    assert get_connector(db, connector_uuid) is None
