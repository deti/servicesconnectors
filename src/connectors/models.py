""" Connector model and functions """

import json
from typing import Optional, Sequence

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src.database import Base

from .schemas import ConnectorCreate
from .utils import generate_uuid_from_dict


class Connector(Base):  # type: ignore
    """Connector model"""

    __tablename__ = "connectors"

    uuid = Column(String(36), primary_key=True, unique=True, nullable=False)
    connector_type = Column(String(50), nullable=False)
    connector_settings = Column(Text, nullable=False)
    description = Column(String(100))
    created_at = Column(
        DateTime, server_default=func.now()  # pylint: disable=not-callable
    )
    modified_at = Column(
        DateTime,
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )


def get_connector(db: Session, connector_uuid: str) -> Optional[Connector]:
    """Get a connector by uuid from Database"""
    return db.query(Connector).filter(Connector.uuid == connector_uuid).first()


def get_all_connectors(db: Session) -> Sequence[Connector]:
    """Get all connectors uuids from Database"""
    return db.query(Connector).all()


def create_connector(
    db: Session, connector_info: ConnectorCreate, connector_uuid: Optional[str] = None
) -> Connector:
    """Create a connector in Database"""
    if connector_uuid is None:
        connector_uuid = generate_uuid_from_dict(connector_info.connector_settings)

    connector = Connector(
        uuid=connector_uuid,
        connector_type=connector_info.connector_type,
        connector_settings=json.dumps(connector_info.connector_settings),
        description=connector_info.description,
    )
    db.add(connector)
    db.commit()
    db.refresh(connector)
    return connector


def get_or_create_connector(db: Session, connector_info: ConnectorCreate) -> Connector:
    """Get or create a connector in Database"""
    item_uuid = generate_uuid_from_dict(connector_info.connector_settings)
    connector = get_connector(db, item_uuid)
    if connector:
        return connector
    return create_connector(db, connector_info, item_uuid)
