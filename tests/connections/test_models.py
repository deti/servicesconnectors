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


def test_get_connection_returns_none_when_non_exsited(db: Session):
    connection = get_connection(db, "test-uuid")
    assert connection is None


def test_get_connection_returns_connection_when_exsited(db: Session):
    connection = fake_connection()
    db.add(connection)
    db.commit()
    db.refresh(connection)

    assert get_connection(db, str(connection.uuid)) == connection


def fake_connection_create() -> ConnectionCreate:
    return ConnectionCreate(
        type=fake.word(),
        settings=fake_appstore_settings(),
        description=fake.sentence(),
    )


def test_create_connection_creates_connection(db: Session):
    connection_create = fake_connection_create()

    connection = create_connection(db, connection_create)

    assert connection.type == connection_create.type
    assert connection.settings == json.dumps(connection_create.settings)
    assert connection.description == connection_create.description


def test_or_create_connection_creates_connection_when_not_exsited(db: Session):
    connection_create = fake_connection_create()

    # No Connect before test
    expected_uuid = generate_uuid_from_dict(connection_create.settings)
    assert get_connection(db, expected_uuid) is None

    # connection created
    connection = get_or_create_connection(db, connection_create)
    assert expected_uuid == connection.uuid
    assert connection.type == connection_create.type
    assert connection.settings == json.dumps(connection_create.settings)
    assert connection.description == connection_create.description


def test_or_create_connection_returns_connection_when_exsited(db: Session):
    connection_create = fake_connection_create()
    created_item = create_connection(db, connection_create)
    retrieved_item = get_or_create_connection(db, connection_create)

    assert retrieved_item == created_item


def test_all_connections_uuids_returns_empty_list_when_no_connection(db: Session):
    assert get_all_connections(db) == []


def test_get_all_connections_returns_all_connectrs(db: Session):
    expected_uuids = [
        create_connection(db, fake_connection_create()) for _ in range(10)
    ]
    assert set(get_all_connections(db)) == set(expected_uuids)


def test_delete_connection_from_db_deletes_connection_when_exsited(db: Session):
    connection = create_connection(db, fake_connection_create())
    connection_uuid = str(connection.uuid)  # avoid mypy error
    assert get_connection(db, connection_uuid) is not None

    delete_connection_from_db(db, connection_uuid)
    assert get_connection(db, connection_uuid) is None
