""" Connector model and functions """

import json
from typing import Optional, Sequence

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src.database import Base

from .schemas import ConnectionCreate
from .utils import generate_uuid_from_dict


class Connection(Base):  # type: ignore
    """Connection model"""

    __tablename__ = "connections"

    uuid = Column(String(36), primary_key=True, unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    settings = Column(Text, nullable=False)
    description = Column(String(100))
    created_at = Column(
        DateTime, server_default=func.now()  # pylint: disable=not-callable
    )
    modified_at = Column(
        DateTime,
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )


def get_connection(db: Session, connection_uuid: str) -> Optional[Connection]:
    """Get a connector by uuid from Database"""
    return db.query(Connection).filter(Connection.uuid == connection_uuid).first()


def get_all_connections(db: Session) -> Sequence[Connection]:
    """Get all connections uuids from Database"""
    return db.query(Connection).all()


def create_connection(
    db: Session, connection_create: ConnectionCreate, connection_uuid: Optional[str] = None
) -> Connection:
    """Create a connection in Database"""
    if connection_uuid is None:
        connection_uuid = generate_uuid_from_dict(connection_create.settings)

    connection = Connection(
        uuid=connection_uuid,
        type=connection_create.type,
        settings=json.dumps(connection_create.settings),
        description=connection_create.description,
    )
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def get_or_create_connection(
    db: Session, connection_create: ConnectionCreate
) -> Connection:
    """Get or create a connection in Database"""
    item_uuid = generate_uuid_from_dict(connection_create.settings)
    connection = get_connection(db, item_uuid)
    if connection:
        return connection
    return create_connection(db, connection_create, item_uuid)


def delete_connection_from_db(db: Session, connecton_uuid: str) -> None:
    """Delete a connecton in Database"""
    connecton = get_connection(db, connecton_uuid)
    if connecton:
        db.delete(connecton)
        db.commit()
