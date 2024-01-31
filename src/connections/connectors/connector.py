""" Connectors interface """

import json
from abc import abstractmethod

from src.connections.models import Connection

class ConnectorException(Exception):
    """Base exception for connectors"""


class Connector:
    """Base connector for data syncronization"""

    def __init__(self, connection: Connection):
        self.connection = connection
        self.item_uuid = connection.uuid
        self.type = connection.type
        self.settings = json.loads(connection.settings)  # type: ignore

    @abstractmethod
    def read_source(self) -> dict:
        """Read source data"""
