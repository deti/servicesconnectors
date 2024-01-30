from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Connector(Base):
    __tablename__ = 'connectors'

    uuid = Column(String(36), primary_key=True, unique=True, nullable=False)
    connector_type = Column(String(50), nullable=False)
    connector_settings = Column(Text, nullable=False)
    description = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

