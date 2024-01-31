""" Connector runner """

from typing import Optional, Type  # noqa: F401

from src.connections.connectors.appstore import AppstoreConnector
from src.connections.connectors.connector import Connector  # noqa: F401
from src.connections.connectors.googleplay import GooglePlayConnector
from src.connections.models import Connection
from src.connections.storage import Storage


class RunnerException(Exception):
    """Runner exception"""


def run_connector(connection: Connection):
    """Run a connector"""
    storage = Storage()

    connector_class = None  # type: Optional[Type[Connector]]
    if connection.type == "appstore":
        connector_class = AppstoreConnector
    elif connection.type == "googleplay":
        connector_class = GooglePlayConnector

    if connector_class is None:
        raise RunnerException(f"Connector {connection.type} not found")

    connector = connector_class(connection)
    data = connector.read_source()

    storage.write(data, connection.uuid)  # type: ignore
