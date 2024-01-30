""" Schemas for connectors. """

from typing import Dict

from pydantic import BaseModel


class ConnectorCreate(BaseModel):
    """Connector create schema"""

    connector_type: str
    connector_settings: Dict[str, str]
    description: str
