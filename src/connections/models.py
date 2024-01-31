""" Connector model and functions """

import json
from typing import Optional, Sequence

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src.database import Base

from .schemas import ConnectorCreate
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


def get_connection(db: Session, connector_uuid: str) -> Optional[Connection]:
    """Get a connector by uuid from Database"""
    return db.query(Connection).filter(Connection.uuid == connector_uuid).first()


def get_all_connections(db: Session) -> Sequence[Connection]:
    """Get all connections uuids from Database"""
    return db.query(Connection).all()


def create_connection(
    db: Session, connector_info: ConnectorCreate, connector_uuid: Optional[str] = None
) -> Connection:
    """Create a connector in Database"""
    if connector_uuid is None:
        connector_uuid = generate_uuid_from_dict(connector_info.settings)

    connector = Connection(
        uuid=connector_uuid,
        type=connector_info.type,
        settings=json.dumps(connector_info.settings),
        description=connector_info.description,
    )
    db.add(connector)
    db.commit()
    db.refresh(connector)
    return connector


def get_or_create_connection(
    db: Session, connector_info: ConnectorCreate
) -> Connection:
    """Get or create a connector in Database"""
    item_uuid = generate_uuid_from_dict(connector_info.settings)
    connector = get_connection(db, item_uuid)
    if connector:
        return connector
    return create_connection(db, connector_info, item_uuid)


def delete_connection_from_db(db: Session, connector_uuid: str) -> None:
    """Delete a connector in Database"""
    connector = get_connection(db, connector_uuid)
    if connector:
        db.delete(connector)
        db.commit()
