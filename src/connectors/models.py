""" Connector model and functions """

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


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
